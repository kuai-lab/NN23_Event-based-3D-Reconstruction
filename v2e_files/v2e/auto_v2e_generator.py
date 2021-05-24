import os
import multiprocessing
import numpy as np

path = "./input/tmpsaveroot/"
file_list = os.listdir(path)

# print ("file_list: {}".format(file_list))
i = 0
output_path = "./output/tmpsaveroot/"
if not os.path.exists(output_path):
                os.mkdir(output_path) 

num_cores = multiprocessing.cpu_count()
print("multiprocessing with",num_cores,"cores")
data = list(range(0,len(file_list)))
splited_data = np.array_split(data,num_cores)
splited_data = [x.tolist() for x in splited_data]
splited_file = []
for nums in splited_data:
	splited_file.append([file_list[idx] for idx in nums])
print(splited_file)


def process(file_list):
    for big_files in file_list:
        big_path = "./input/tmpsaveroot/" + big_files
        output_path = "./output/tmpsaveroot/" + big_files
        if not os.path.exists(output_path):
    	        os.mkdir(output_path) 
    
        small_file_list = os.listdir(big_path)

        for small_files in small_file_list:
    	# print ("file_list: {}".format(small_files))
            video_path = "./input/tmpsaveroot/" + big_files + '/' + small_files
            output_path = "./output/tmpsaveroot/" + big_files + '/' + small_files
            if not os.path.exists(output_path):
	            os.mkdir(output_path)
            video_path_list = os.listdir(video_path)

            for videos in video_path_list:
	        # print ("file_list: {}".format(videos))
                input = video_path +'/'+videos
                output_path = "./output/tmpsaveroot/" + big_files + '/' + small_files + '/' + videos + '/'
                if not os.path.exists(output_path):
                    os.mkdir(output_path) 

	    
                print ("file_list: {}".format(input))
                os.system('python v2e.py -i ' + input + ' --overwrite --timestamp_resolution=.003 --auto_timestamp_resolution=False --dvs_exposure duration 0.005 --output_folder=' + output_path + ' --overwrite --pos_thres=.15 --neg_thres=.15 --sigma_thres=0.03 --dvs_aedat2 video.aedat --output_width=346 --output_height=260 --stop_time=3 --cutoff_hz=15 --disable_slomo')
    
            print("--------------------------")
    print("---V2E Completed!!---")

pool = multiprocessing.Pool(processes=num_cores)
pool.map(process,splited_file)

