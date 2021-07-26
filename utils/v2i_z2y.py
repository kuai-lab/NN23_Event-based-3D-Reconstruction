import numpy as np
import glob
import cv2
import os

npz_flie = glob.glob("*.npz")
video = cv2.VideoCapture("0000-1439.avi")

os.makedirs("./depth/data", exist_ok=True)
os.makedirs("./depth/data", exist_ok=True)


for idx, npz in enumerate(npz_flie):
    npz_file = np.load(npz)
    np.save("depth/data/depth_{:010d}".format(idx), npz_file["depth_map"])
    ret, frame = video.read()
    cv2.imwrite("rgb/data/frame_{:010d}.png".format(idx), frame)

video.release()
