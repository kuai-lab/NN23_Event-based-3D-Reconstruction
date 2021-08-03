import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

import os
import time
import random

from constrain_moments import K2M

class Logit(nn.Module):
    def forward(self, input: torch.Tensor) -> torch.Tensor:
        input = torch.clamp(input, min=0, max=1)
        return torch.logit(input/2 + 0.5)
    
class Sigmoid(nn.Module):
    def forward(self, input: torch.Tensor) -> torch.Tensor:
        return (torch.sigmoid(input)-0.5)*2
    
sig = Sigmoid()
log = Logit()

# reference : https://github.com/CoinCheung/pytorch-loss/blob/master/focal_loss.py
class my_loss(nn.Module):
    def __init__(self,
                 device,
                 alpha=0.75,
                 beta=0.9,
                 gamma=2,
                 ):
        super(my_loss, self).__init__()
        self.device = device
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma

    def forward(self, logits, label):
        if len(logits.shape) == 5: x = logits.squeeze(1)
        else:x = logits
        if len(label.shape) == 5: y = label.squeeze(1)
        else:y = label

        # compute loss
        props = torch.sigmoid(x)
        weight_alpha = -1*self.alpha
        log_probs = torch.where(x >= 0,
                F.softplus(x, -1, 50),
                x - F.softplus(x, 1, 50))
        log_1_probs = torch.where(x >= 0,
                -x + F.softplus(x, -1, 50),
                -F.softplus(x, 1, 50))
        label_1_beta = (1-y) ** self.beta
        probs_gamma = props ** self.gamma
        probs_1_gamma = (1-props) ** self.gamma

        pos = weight_alpha * probs_1_gamma * log_probs
        neg = weight_alpha * 0.05 * label_1_beta * probs_gamma * log_1_probs

        result = torch.where(y == 1, pos, neg)
#        zero_mask = torch.zeros(result.shape).to(self.device)
#        result = torch.where(y == 0, zero_mask, result)
#        mask = torch.where(y == 1)
        mask = torch.isnan(result)
        result = torch.where(mask, mask*1e-9, result)

        loss = result.mean()
        return loss
        
def train_on_batch(device, input_tensor, target_tensor, model, optimizer, criterion, teacher_forcing_ratio, constraints, recurrent):  
    model.train()
    optimizer.zero_grad()
    
    input_length  = input_tensor.size(1)
    target_length = target_tensor.size(1)
    loss = 0

    if recurrent:
        outputs = model(input_tensor[:,:,:,:,:])
        loss += criterion(outputs,target_tensor[:,0,:,:,:].unsqueeze(1))
       
        use_teacher_forcing = True if random.random() < teacher_forcing_ratio else False 
        for ei in range(1,input_length):
            if use_teacher_forcing:
                outputs = torch.cat((model(torch.cat((input_tensor[:,ei:,:,:,:],target_tensor[:,:ei,:,:,:]),1)),outputs),1)
                loss += criterion(outputs[:,-1,:,:,:],target_tensor[:,ei,:,:,:])
            else:
                outputs = torch.cat((model(torch.cat((input_tensor[:,ei:,:,:,:],outputs),1)),outputs),1)
                loss += criterion(outputs[:,-1,:,:,:],target_tensor[:,ei,:,:,:])
        
    else:
        outputs = model(input_tensor)
        loss += criterion(outputs,target_tensor)
        
    #print('fin',loss.item() / target_length)
    loss.backward()
    optimizer.step()
    return loss.item() / target_length


def train_iter(device, model, nepochs, train_loader, lr =0.0001, recurrent=False, focal=False):
    best_mse = float('inf')
    optimizer = torch.optim.Adam(model.parameters(),lr=lr)
    criterion = nn.MSELoss()
    if focal: criterion = my_loss(device)

    constraints = torch.zeros((49,7,7)).to(device)
    ind = 0
    for i in range(0,7):
        for j in range(0,7):
            constraints[ind,i,j] = 1
            ind +=1
            
    for epoch in range(nepochs):
        t0 = time.time()
        loss_epoch = 0
        teacher_forcing_ratio = np.maximum(0 , 1 - epoch * 0.003) 

        for i, (x,y) in enumerate(train_loader, 0):
            input_tensor = x[:,:,:,45:-45,2:-2].to(device).float()
            target_tensor = y[:,:,:,45:-45,2:-2].to(device).float()

            #if focal:
            on_input_y = torch.ones(input_tensor[:,:,0,:,:].shape).to(device).float()
            off_input_y = torch.ones(input_tensor[:,:,1,:,:].shape).to(device).float()

            on_input_tensor = torch.where(input_tensor[:,:,0,:,:] == 0, input_tensor[:,:,0,:,:], on_input_y)
            off_input_tensor = torch.where(input_tensor[:,:,1,:,:] == 0, input_tensor[:,:,1,:,:], off_input_y)

            input_tensor = torch.cat([on_input_tensor.unsqueeze(2), off_input_tensor.unsqueeze(2)], 2)

            on_target_y = torch.ones(target_tensor[:,:,0,:,:].shape).to(device).float()
            off_target_y = torch.ones(target_tensor[:,:,1,:,:].shape).to(device).float()

            on_target_tensor = torch.where(target_tensor[:,:,0,:,:] == 0, target_tensor[:,:,0,:,:], on_target_y)
            off_target_tensor = torch.where(target_tensor[:,:,1,:,:] == 0, target_tensor[:,:,1,:,:], off_target_y)

            target_tensor = torch.cat([on_target_tensor.unsqueeze(2), off_target_tensor.unsqueeze(2)], 2)
                
            loss = train_on_batch(device, input_tensor, target_tensor, model, optimizer, criterion, teacher_forcing_ratio, constraints, recurrent)                                   
            loss_epoch += loss

            print('epoch ',epoch + 1,  ' loss ',loss_epoch, ' time epoch ',time.time()-t0)