import cv2
import glob
import re
import natsort
import numpy as np

obj_list = ['beachball']#, 'rugbyball', 'golfball', 'tennisball', 'baseball', 'basketball', 'beachball', 'volleyball', 'masterball', 'soccerball']
angle_list = [0, 15, 30, 45, 60, 75, 90]
for obj in obj_list:
    for angle in angle_list:
        file_list = natsort.natsorted(glob.glob('./{}_{}/*.npz'.format(obj, angle)))
        height, width, layers = np.load(file_list[0])["normal_map"].shape
        size = (width,height)
        out = cv2.VideoWriter('./video_result/{}_{}.avi'.format(obj, angle),cv2.VideoWriter_fourcc(*'XVID'), 480, size)

        for filename in file_list:
            img = np.load(filename)["normal_map"]
            img = np.uint8((img - img.min()) / (img.max() - img.min()) * 255)
            black_mask = np.where((img[:,:,0]==img[:,:,1])&(img[:,:,1]==img[:,:,2])&(img[:,:,0]==img[:,:,2]))
            img[black_mask[0],black_mask[1],:]=0
            out.write(img)

out.release()
