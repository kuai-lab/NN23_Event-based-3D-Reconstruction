import glob
import os
import flow_vis

folder_list = glob.glob("result/*_*_result")

for folder in folder_list:
    os.remove(folder+"/depth/data/depth_0000001439.npy")
    os.remove(folder+"/rgb/data/frame_0000001439.png")
