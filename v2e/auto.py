import os
import multiprocessing
import numpy as np
import time
import matplotlib.pyplot as plt
import pandas as pd

def events_to_voxel_grid(events, num_bins=5, width=346, height=260):
    """
    Build a voxel grid with bilinear interpolation in the time domain from a set of events.
    :param events: a [N x 4] NumPy array containing one event per row in the form: [timestamp, x, y, polarity]
    :param num_bins: number of bins in the temporal axis of the voxel grid
    :param width, height: dimensions of the voxel grid
    """

    assert(events.shape[1] == 4)
    assert(num_bins > 0)
    assert(width > 0)
    assert(height > 0)

    voxel_grid = np.zeros((num_bins, height, width), np.float32).ravel()

    # normalize the event timestamps so that they lie between 0 and num_bins
    last_stamp = events[-1, 0]
    first_stamp = events[0, 0]
    deltaT = last_stamp - first_stamp

    if deltaT == 0:
        deltaT = 1.0

    events[:, 0] = (num_bins - 1) * (events[:, 0] - first_stamp) / deltaT
    ts = events[:, 0]
    xs = events[:, 1].astype(np.int)
    ys = events[:, 2].astype(np.int)
    pols = events[:, 3]
    pols[pols == 0] = -1  # polarity should be +1 / -1

    tis = ts.astype(np.int)
    dts = ts - tis
    vals_left = pols * (1.0 - dts)
    vals_right = pols * dts

    valid_indices = tis < num_bins
    np.add.at(voxel_grid, xs[valid_indices] + ys[valid_indices] * width +
              tis[valid_indices] * width * height, vals_left[valid_indices])

    valid_indices = (tis + 1) < num_bins
    np.add.at(voxel_grid, xs[valid_indices] + ys[valid_indices] * width +
              (tis[valid_indices] + 1) * width * height, vals_right[valid_indices])

    voxel_grid = np.reshape(voxel_grid, (num_bins, height, width))

    return voxel_grid

def make_voxel_grid(path, events, times, width=346, height=260):
    voxel_grid = np.zeros((len(times), height, width), np.float32)

    for idx, time in enumerate(times[:,1]):
        if idx == 0: indices = np.where(events[:, 0]<time)[0]
        else: indices = np.where((times[idx-1,1]<events[:, 0]) & (events[:, 0]<time))[0]

        np.save(path +'/'+ "event_tensor_{:010d}".format(idx), events_to_voxel_grid(events[indices,:]))
#        voxel_grid[idx, :] =events_to_voxel_grid(events[indices,:])
#        rb_voxel = np.ones((height, width, 3), np.float32)
#        red = np.where(voxel_grid[idx]>0)
#        blue = np.where(voxel_grid[idx]<0)
#        rb_voxel[red[0],red[1],1:] -= 1
#        rb_voxel[blue[0],blue[1],:2] -= 1
#        plt.imshow(rb_voxel)
#        plt.show()
 
    return 0

def voxel_timestamp(path, original):
    loss = np.array([])
    for i in range(len(original)-1):
        loss = np.append(loss, np.array(original['time'][i+1] - original['time'][i]))
    #     print(np.array(original['time'][i+1] - original['time'][i]))
    avg = np.mean(loss)
    #print(avg)
    first = []
    for i in range(len(original)):
        a = original['time'][i] - avg
        first.append(a)
        #print(a)
    first = pd.DataFrame(first)
    boundary_from_v2e = pd.concat([first, original], axis = 1)
    boundary_from_v2e = boundary_from_v2e.drop(['frame'], axis=1)
    boundary_from_v2e.to_csv(path +'/'+'boundary_timestamps.txt', header=None, sep =' ')
    original.to_csv(path +'/'+ 'timestamps.txt', header=None, index=False,sep =' ')

# V2E
input_path = "/home/kcy/Desktop/nerf/input/"
output_path = "/home/kcy/Desktop/nerf/output/"

file_list = os.listdir(input_path)

for files in file_list:
    big_path = "/home/kcy/Desktop/nerf/input/" + files
    output_path = "/home/kcy/Desktop/nerf/output/" + files

    if not os.path.exists(output_path):
        os.mkdir(output_path) 
    os.system('python v2e.py -i ' + big_path +' --overwrite --timestamp_resolution=.003 --auto_timestamp_resolution=False --dvs_exposure duration 0.00208 --output_folder=' + output_path +' --overwrite --pos_thres=.15 --neg_thres=.15 --sigma_thres=0.03 --dvs_aedat2 bunny.aedat --output_width=346 --output_height=260 --stop_time=3 --cutoff_hz=15 --disable_slomo')
    print(files + 'v2e done! saves to '+output_path)
print('v2e done')

# 'python v2e.py -i ' + big_path +' --overwrite --timestamp_resolution=.003 --auto_timestamp_resolution=False --dvs_exposure duration 0.00208333 --output_folder=' + output_path +' --overwrite --pos_thres=.15 --neg_thres=.15 --sigma_thres=0.03 --dvs_aedat2 bunny.aedat --output_width=346 --output_height=260 --stop_time=3 --cutoff_hz=15 --disable_slomo --dvs_params clean'

input_path = "/home/kcy/Desktop/nerf/output/"
file_list = os.listdir(input_path)

lengh = len(file_list)
i = 0

print('files to be proceed : ', lengh)
for files in file_list:
    i += 1
    path = input_path+files+'/'
    voxel_path = path+'voxels'
    if not os.path.exists(voxel_path):
        os.mkdir(voxel_path) 
    print(voxel_path + '  started!')
    
    times = np.loadtxt(path + "dvs-video-frame_times.txt")
    events = np.loadtxt(path + "v2e-dvs-events.txt")
    original = pd.read_csv(path +'dvs-video-frame_times.txt', sep='\t',  
                       skiprows = [0, 1], names = ['frame', 'time'])
    voxel_grid = make_voxel_grid(voxel_path, events, times)
    voxel_time = voxel_timestamp(voxel_path, original)
    print(voxel_path + '  done!')
    print('process:', i,'/',lengh)
    print('\n')

