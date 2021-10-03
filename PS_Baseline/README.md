# PS-FCN
**[PS-FCN: A Flexible Learning Framework for Photometric Stereo, ECCV 2018](https://guanyingc.github.io/PS-FCN/)**,
<br>

This paper addresses the problem of learning based photometric stereo for non-Lambertian surface.
<br>


## Overview
We provide:
- Datasets: Blobby dataset (4.7 GB), Sculpture dataset (19 GB)
- Trained models (on both the Blobby dataset and the Sculpture dataset with a per-sample input number of 32):
    - PS-FCN for calibrated photometric stereo
    - UPS-FCN for uncalibrated photometric stereo
- Code to test on DiLiGenT main dataset
- Code to train a new model

If the above command is not working, please manually download the trained models from Google Drive ([PS-FCN and UPS-FCN](https://drive.google.com/drive/folders/1VxrPsV8Pg28JCcMZklW1LcBFm4crhK0F?usp=sharing)) and put them in `./data/models/`.

#### Test on the DiLiGenT main dataset
```shell
# Download DiLiGenT main dataset
sh scripts/prepare_diligent_dataset.sh

# Test PS-FCN on DiLiGenT main dataset using all of the 96 image-light pairs
CUDA_VISIBLE_DEVICES=0 python eval/run_model.py --retrain data/models/PS-FCN_B_S_32.pth.tar --in_img_num 96
# You can find the results in data/Training/run_model/

# Test UPS-FCN on DiLiGenT main dataset only using images as input 
CUDA_VISIBLE_DEVICES=0 python eval/run_model.py --retrain data/models/UPS-FCN_B_S_32.pth.tar --in_img_num 96 --in_light
```

## Training
To train a new PS-FCN model, please follow the following steps:
#### Download the training data
```shell
# The total size of the zipped synthetic datasets is 4.7+19=23.7 GB 
# and it takes some times to download and unzip the datasets.
sh scripts/download_synthetic_datasets.sh
```
If the above command is not working, please manually download the training datasets from Google Drive ([PS Sculpture Dataset and PS Blobby Dataset](https://drive.google.com/drive/folders/1VxrPsV8Pg28JCcMZklW1LcBFm4crhK0F?usp=sharing)) and put them in `./data/datasets/`. 

#### Train PS-FCN and UPS-FCN
```shell
# Train PS-FCN on both synthetic datasets using 32 images-light pairs
CUDA_VISIBLE_DEVICES=0 python main.py --concat_data --in_img_num 32

# Train UPS-FCN on both synthetic datasets using 32 images
CUDA_VISIBLE_DEVICES=0 python main.py --concat_data --in_img_num 32 --in_light --item uncalib

# Please refer to options/base_opt.py and options/train_opt.py for more options

# You can find checkpoints and results in data/Training/
```

#### Test on the DiLiGenT main dataset
```shell
CUDA_VISIBLE_DEVICES=0 python eval/run_model.py --retrain data/models/PS-FCN.pth.tar --in_img_num 96 --train_img_num 32
# You can find the results in data/Training/run_model
```

## Data Normalization for Handling SVBRDFs (TPAMI 2020)
```shell
# Train
CUDA_VISIBLE_DEVICES=0 python main.py --concat_data --in_img_num 32 --in_light --normalize --item normalize

# Test
CUDA_VISIBLE_DEVICES=0 python eval/run_model.py --retrain data/models/PS-FCN_B_S_32_normalize.pth.tar --in_img_num 96 --normalize --train_img_num 32
```
