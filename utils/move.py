import os
import glob
import tqdm
import shutil
import numpy as np

before_folder_list = glob.glob("*_*.avi")

for before_folder in tqdm.tqdm(before_folder_list):
    obj = before_folder.split("_")[0]
    angle = before_folder.split("_")[1].split(".")[0]

    voxel = os.path.join(before_folder, "voxels")
    shutil.move(voxel, os.path.join("result", "{}_{}_result".format(obj, angle)))

    events = np.loadtxt(os.path.join(before_folder, "v2e-dvs-events.txt"))
    timestamp = np.loadtxt(os.path.join(before_folder, "dvs-video-frame_times.txt"))
    os.makedirs("./result/{}_{}_result/events/data".format(obj, angle), exist_ok=True)

    for idx, time in enumerate(timestamp[:,1]):
        if idx == 0: indices = np.where(events[:, 0]<time)[0]
        else: indices = np.where((timestamp[idx-1,1]<events[:, 0]) & (events[:, 0]<time))[0]
        events[np.where(events[indices,3]==0)[0],3]=-1.0
        np.save("./result/{}_{}_result/events/data/events_{:010d}".format(obj, angle, idx), events[indices,:])

    timestamp_txt = os.path.join("result", "{}_{}_result".format(obj, angle), "voxels", "timestamps.txt")
    shutil.copy(timestamp_txt, os.path.join("result", "{}_{}_result".format(obj, angle), "depth", "data","timestamps.txt"))
    shutil.copy(timestamp_txt, os.path.join("result", "{}_{}_result".format(obj, angle), "rgb", "data","timestamps.txt"))
    shutil.copy(timestamp_txt, os.path.join("result", "{}_{}_result".format(obj, angle), "events", "data","timestamps.txt"))

