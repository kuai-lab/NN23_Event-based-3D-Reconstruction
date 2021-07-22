# Depth map to 3D Point Cloud Conversion
(Update date : 22 Jul. 2021)  
Generating 3D point cloud from depth map with virtual camera's parameter.

## Requirement
- MacOS or Linux (Ubuntu recommended)
- Python 3 (Conda virtual environment recommended)
  - natsort
  - open3d

## Installation & Run

### Using Anaconda

- Setup the anaconda virtual environment and installing requirements
```
git clone https://github.com/kuai-lab/Event-based-3D-Reconstruction
conda create -n <env_name> python=3.8
conda activate <env_name>
pip install -r requirements.txt
```
### Run demo

- You can input your data which composed with *.npz format, it may include depth map, intrinsic parameter and extrinsic parater per frames.
- Put your input data in ```depth2pc/data``` directory, run ```point_cloud_generator.py``` with direction below.
- Your point cloud data will be stored in ```depth2pc/output``` directory as *.ply format.
```
cd depth2pc
python point_cloud_generator.py
```

### (Additional) Run in Notebook

- We also. provide this generator as notebook. You can show in [Notebook](jupyter/point_cloud_generator.ipynb)
