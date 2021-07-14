from pyntcloud import PyntCloud
import copy
import numpy as np
import open3d as o3d

from numpy import load
import pandas as pd

cloud = PyntCloud.from_file("bunny.obj")

#cloud.add_scalar_field("hsv")

voxelgrid_id = cloud.add_structure("voxelgrid", n_x=32, n_y=32, n_z=32)
new_cloud = cloud.get_sample("voxelgrid_nearest", voxelgrid_id=voxelgrid_id, as_PyntCloud=True)
new_cloud.to_file("bunny.npz")
data = load('bunny.npz')
lst = data.files
arr = []
for item in lst:
    #print(item)
    arr = data[item]
arr = np.array(arr)
# print(type(arr))

df = pd.DataFrame(arr)
df = df.iloc[:,:-1]
# print(df)
df = np.array(df)
#print(df)
np.save("bunny.npy", df)
print("Saved npy")