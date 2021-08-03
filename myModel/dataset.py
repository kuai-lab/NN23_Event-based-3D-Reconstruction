import os
import h5py
import numpy as np
import glob

class event_data:
    def __init__(self, PATH, window_size, pred_size, stride, tiny=False, train=True):
        self.tiny = tiny
        self.window_size = window_size
        self.pred_size = pred_size
        self.data = []
        self.n_windows = []
        
        with open(PATH + ('train_path.txt' if train else 'test_path.txt'), 'r') as f:
            while True:
                line = f.readline()
                if not line: break
                strings = line.split('/')[-1].split('.')[0].split('_')
                strings = strings[0]+'_'+strings[1]

                if(line.split(',')[1].find('l')!=-1):
                    exists = sorted(glob.glob(PATH + strings + '/*left*.npy'))[int(line.split(',')[-2]):int(line.split(',')[-1])]
                    if(self.tiny):
                        self.data.append(exists[:len(exists)//3])
                        self.n_windows.append((len(exists[:len(exists)//3])-window_size)//stride + 1)
                    else:
                        self.data.append(exists)
                        self.n_windows.append((len(exists) - window_size - pred_size)//stride + 1)
                        
                if(line.split(',')[1].find('r')!=-1):
                    exists = sorted(glob.glob(PATH + strings + '/*right*.npy'))[int(line.split(',')[-2]):int(line.split(',')[-1])]
                    if(self.tiny):
                        self.data.append(exists[:len(exists)//3])
                        self.n_windows.append((len(exists[:len(exists)//3])-window_size)//stride + 1)
                    else:
                        self.data.append(exists)
                        self.n_windows.append((len(exists) - window_size - pred_size)//stride + 1)
        print(self.n_windows)
    
    def __getitem__(self, idx):
        i = 0
        x = []
        y = []
        for count in self.n_windows:
            if(count<=idx):
                idx = idx - count
                i += 1
            else:
                break
                
        for j in range(self.window_size):
            #print(self.data[i][idx+j])
            x.append(np.load(self.data[i][idx+j]))
            
        for j in range(self.pred_size):
            #print(self.data[i][idx+self.window_size+j])
            y.append(np.load(self.data[i][idx+self.window_size+j]))
            
        return np.array(x), np.array(y)
    
    def __len__(self):
        return sum(self.n_windows)