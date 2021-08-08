import numpy as np
import glob
import cv2
import os
import natsort

folder_list = glob.glob("*_*")

for folder in folder_list:
    npz_flie = natsort.natsorted(glob.glob("./{}/*.npz".format(folder)))

    os.makedirs("./{}_result/depth/data".format(folder), exist_ok=True)
    os.makedirs("./{}_result/rgb/data".format(folder), exist_ok=True)

    for idx, npz in enumerate(npz_flie):
        npz_file = np.load(npz)
        np.save("./{}_result/depth/data/depth_{:010d}".format(folder, idx), npz_file["depth_map"])
        img = npz_file["normal_map"]
        img = np.uint8((img - img.min()) / (img.max() - img.min()) * 255)
        black_mask = np.where((img[:,:,0]==img[:,:,1])&(img[:,:,1]==img[:,:,2])&(img[:,:,0]==img[:,:,2]))
        img[black_mask[0],black_mask[1],:]=0
        cv2.imwrite("./{}_result/rgb/data/frame_{:010d}.png".format(folder, idx), img)
