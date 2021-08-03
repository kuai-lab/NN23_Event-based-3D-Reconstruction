import os
import argparse

import torch

from dataset           import event_data
from model.Transformer import Transformer
from experiments       import train_iter

def str2bool(v):
    if isinstance(v, bool):return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'): return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'): return False
    else: raise argparse.ArgumentTypeError('Boolean value expected.')

parser = argparse.ArgumentParser(description='Train models.')
parser.add_argument('--device', type=int,
                    help="Num of gpu device")
parser.add_argument('--path', type=str,
                    help="path to dataset")
parser.add_argument('--batch_size', type=int, default=10,
                    help="batch_size, default=10")
parser.add_argument('--epochs', type=int, default=100,
                    help="train epochs, default=100")
parser.add_argument('--eval', type=int,
                    help="eval per epoch")
parser.add_argument('--load', type=str,
                    help="if you want to load, input something")
parser.add_argument('--lr', type=float, default=0.0001,
                    help="lr, default=1e-4")
parser.add_argument('--recur', default=False, type=str2bool,
                    help="recurrent")

args = parser.parse_args()


os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"   
os.environ["CUDA_VISIBLE_DEVICES"]=str(args.device)

model_type = "transformer"


PATH       = args.path
batch_size = args.batch_size

train_dataset = event_data(PATH, window_size=4, pred_size=4, stride=1, train=True)
train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=batch_size)
print("dataset loaded")

for i,(x,y) in enumerate(train_loader):
    print("train_loader",i,x.shape,y.shape)
    break


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(model_type, 'batch_size='+str(batch_size))

model = Transformer()
model.to(device)

print("model loaded")


def count_parameters(model): return sum(p.numel() for p in model.parameters() if p.requires_grad)
print('params :', count_parameters(model))

print("train start")
train_iter(device, model, args.epochs, train_loader, lr=args.lr, recurrent=args.recur)