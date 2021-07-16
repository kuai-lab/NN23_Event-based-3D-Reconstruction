from pyntcloud import PyntCloud
import copy
import numpy as np
import os
from numpy import load
import pandas as pd

def meshtopc(name):
    cloud = PyntCloud.from_file("obj/{}".format(name))

    voxelgrid_id = cloud.add_structure("voxelgrid", n_x=32, n_y=32, n_z=32)
    new_cloud = cloud.get_sample("voxelgrid_nearest", voxelgrid_id=voxelgrid_id, as_PyntCloud=True)
    new_cloud.to_file("npz/{}.npz".format(name))
    data = load('npz/{}.npz'.format(name))
    lst = data.files
    arr = []
    for item in lst:
        arr = data[item]
    arr = np.array(arr)

    df = pd.DataFrame(arr)
    df = df.iloc[:,:-1]
    df = np.array(df)

    np.save("npy/{}.npy".format(name), df)

def main():
    path = "./obj"
    file_list = os.listdir(path)

    for i in range(len(file_list)):
        meshtopc(file_list[i])
        print(file_list[i])

if __name__ == "__main__":
    main()
    print("Saved npy in npy folder")