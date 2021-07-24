import glob
import numpy as np
from tqdm import tqdm

# pip install natsort
import natsort # for index sorting

# pip install open3d
import open3d as o3d # for 3D Point cloud save & visualization

# should be located with same directory
from util.utility import npz_data, generate_pointcloud


# PATH that contains *.npz, *.npy files including camera parameters and depth map, etc.
npz_path_dir = './data/circle/'

npz_list = natsort.natsorted(glob.glob(npz_path_dir+'*.npz'))

print('Ascending sorted by natsort.')
print(len(npz_list))

i_list=[] # List for virtual camera's intrinsic parameter
e_list=[] # List for virtual camera's extrinsic parameter with each frames
d_list=[] # List for virtual camera's predict depth map with each event voxels

### Extracting *.npz 
for idx, npz in enumerate(npz_list):
    i, e, d = npz_data(npz)
    i_list.append(i)
    e[:,3]=(e[:,3]/1000)
    e_list.append(e)
    d_list.append(d)

result = []

print('Generate point cloud with %d input depth maps.' %(len(i_list)))
for i in tqdm(range(len(d_list))):
    # Read depth map, camera parameters
    # Generate point cloud with depth map, intrinsic parameters
    # Registrate point cloud by calculating of extrinsic parameters
    A = generate_pointcloud(d_list[i], i_list[i], e_list[i], 1000)

    if len(result) != 0: 
        result = np.vstack((A, result))
    else: 
        result = A

print('Point cloud generated with %d vertices.' %(len(result)))

pcd_np = np.vstack(result)
pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(pcd_np)

# You can set your output_path and file name
output_path = "./output/"
file_name = "point_cloud.ply"
o3d.io.write_point_cloud(output_path + file_name, pcd)
print("%s successfully stored." %file_name)