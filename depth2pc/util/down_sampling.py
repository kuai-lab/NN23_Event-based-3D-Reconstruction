import open3d as o3d
import numpy as np

# Return numpy array with (Num of points, 3)
def voxel_downsampling(ply_path, voxel_size):
    pcd = o3d.io.read_point_cloud(ply_path)
    print("Downsample the point cloud with a voxel of %f"%voxel_size)
    downpcd = pcd.voxel_down_sample(voxel_size)
    print("before : ", np.asarray(pcd.points).shape)

    print("after : ", np.asarray(downpcd.points).shape)
    print("Sampled ratio : %.2f%%" %(np.asarray(downpcd.points).shape[0]/np.asarray(pcd.points).shape[0]*100))

    return np.asarray(downpcd.points)