import os
import numpy as np


os.makedirs("./events/data", exist_ok=True)

events = np.loadtxt("v2e-dvs-events.txt")
timestamp = np.loadtxt("dvs-video-frame_times.txt")


for idx, time in enumerate(timestamp[:,1]):
    if idx == 0: indices = np.where(events[:, 0]<time)[0]
    else: indices = np.where((timestamp[idx-1,1]<events[:, 0]) & (events[:, 0]<time))[0]
    events[np.where(events[indices,3]==0)[0],3]=-1.0
    np.save("events/data/events_{:010d}".format(idx), events[indices,:])
