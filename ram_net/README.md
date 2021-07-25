# Ramnet 학습 방법

<br>

원정s local 기준

## 0. data 경로
data (voxels는 events경로에 있는 것 복사)
```
|__ wj
    |_ output
    |_ train_data
       |_ depth
          |_ data
          |_ frames
          |_ voxels
       |_ events
          |_ data
          |_ frames
          |_ frames_white
          |_ voxels
       |_ rgb
          |_ data
          |_ voxels
```

## 1. terminal에서 export
```bash
export PREPROCESSED_DATASETS_FOLDER=/data/wj/example
```
## 2. config 내에서 train, validation 경로 수정
```bash
"base_folder": "",
"depth_folder": "depth/data",
"frame_folder": "rgb/data",
"flow_folder": "",
"event_folder": "events/voxels",
```

## 3. config 내에서 train output 경로 수정
```bash
"save_dir": "/data/wj/output",
```

## 4. train.py, model/metric.py 수정
- https://github.com/uzh-rpg/rpg_ramnet/issues/1

## 5. data_loader/event_dataset.py line 142 부분 아래와 같이 수정
```
path_event = glob.glob(self.event_folder + '/*_{:04d}_voxel.npy'.format(self.first_valid_idx + i))

                                            ▽

path_event = glob.glob(self.event_folder + '/event_tensor_{:010d}.npy'.format(self.first_valid_idx + i))
path_event += glob.glob(self.event_folder + '/events_{:010d}.npy'.format(self.first_valid_idx + i))
```

## 5. data_loader/dataset.py line 288 부분 아래와 같이 수정
```
path_depthframe = glob.glob(self.depth_folder + '/*_{:04d}_depth.npy'.format(frame_idx))

                                            ▽

path_depthframe = glob.glob(self.depth_folder + '/depth_{:010d}.npy'.format(frame_idx))
```

## 6. data_loader/dataset.py line 353 부분 아래와 같이 수정
```
path_rgbframe = glob.glob(self.frame_folder + '/*_{:04d}_image.png'.format(frame_idx-(k+1)))

                                            ▽

path_rgbframe = glob.glob(self.frame_folder + '/frame_{:010d}.png'.format(frame_idx - (k + 1)))
```
## 7. data_loader/dataset.py line 384 부분 아래와 같이 수정
```
path_rgbframe = glob.glob(self.frame_folder + '/*_{:04d}_image.png'.format(frame_idx))

                                            ▽

path_rgbframe = glob.glob(self.frame_folder + '/frame_{:010d}.png'.format(frame_idx))
```
## 8. utils/training_utils.py line 99 ~ 101 부분 아래와 같이 수정
```
ave_grads.append(lr*p.grad.abs().mean())
max_grads.append(lr*p.grad.abs().max())
min_grads.append(lr*p.grad.abs().min())
                                            ▽
ave_grads.append(lr*p.grad.abs().mean().cpu())
max_grads.append(lr*p.grad.abs().max().cpu())
min_grads.append(lr*p.grad.abs().min().cpu())



