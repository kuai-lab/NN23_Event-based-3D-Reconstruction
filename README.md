# Event based 3D Reconstruction

Event based 3D Object Reconstruction 연구 Repository입니다.
![image](https://user-images.githubusercontent.com/44921488/125921177-210e8939-f4f0-467a-8e05-812a64d8aed1.png)

# Optical Flow & Depth Map GT
## 1. requirements
### Blender 설치
- https://www.blender.org/

## 2. Blender에 Vision Blender Addon 추가
- Github : https://github.com/Cartucho/vision_blender

## 3. Obj file 불러오기


## 4. Python script 작성
- 처음 시작 option 설정
```
bpy.context.scene.vision_blender.bool_save_gt_data = True
bpy.context.scene.render.engine = 'CYCLES'
cam = scene.objects['Camera']
cam.location = (0, 4.0, 0.5) #카메라 초기 위치 설정
```

- object 마다 pass_index 설정
```
bpy.context.object.pass_index = 1
```
- Camera Pose json 출력

```
frame_data = {
        'file_path': scene.render.filepath,
        'rotation': radians(stepsize),
        'transform_matrix': listify_matrix(cam.matrix_world)
    }
```

- render 시작 (npz 생성)
```
bpy.ops.render.render()
```

### example
- code
```
PLZ add here.
```

### example imgs
- normal<br>
![image](https://user-images.githubusercontent.com/51734430/125779800-15cf838f-2c8c-42cf-8527-aaf6be556187.png)
<br>

- optical flow<br>
![image](https://user-images.githubusercontent.com/51734430/125779642-8b651506-0525-48cc-b6b7-9a9eb993955d.png)
<br>

- depth map<br>
![image](https://user-images.githubusercontent.com/51734430/125779667-091b9fe2-4500-455b-a799-78996f0381d4.png)
<br>

## 5.  

# Mesh to Point Cloud
[레포지토리 이동하기](https://github.com/kuai-lab/Event-based-3D-Reconstruction/tree/main/mesh2pc)
# Event Signal


[v2e github](https://github.com/SensorsINI/v2e)  
```
git clone https://github.com/SensorsINI/v2e.git
cd v2e
```
v2e 폴더에 들어갑니다.  
```
conda create -n v2e-env python=3.8  # create a new environment
source activate v2e-env  # activate the environment
python setup.py develop
```
위 과정으로 v2e를 위한 환경 설정을 마칩니다.
[저자 제공 샘플 데이터 다운](https://drive.google.com/file/d/1dNUXJGlpEM51UVYH4-ZInN9pf0bHGgT_/view?usp=sharing)해당 데이터를 input 폴더를 만들고 안에 넣어줍니다.
```
python v2e.py -i input/tennis.mov --overwrite --timestamp_resolution=.003 --auto_timestamp_resolution=False --dvs_exposure duration 0.005 --output_folder=output/tennis --overwrite --pos_thres=.15 --neg_thres=.15 --sigma_thres=0.03 --dvs_aedat2 tennis.aedat --output_width=346 --output_height=260 --stop_time=3 --cutoff_hz=15 
```
위 명령어를 입력해 v2e를 실행합니다.  
slomo를 사용하지 않으려면
```
python v2e.py -i input/tennis.mov --overwrite --timestamp_resolution=.003 --auto_timestamp_resolution=False --dvs_exposure duration 0.005 --output_folder=output/tennis --overwrite --pos_thres=.15 --neg_thres=.15 --sigma_thres=0.03 --dvs_aedat2 tennis.aedat --output_width=346 --output_height=260 --stop_time=3 --cutoff_hz=15 --disable_slomo
```
위 명령어를 입력합니다.

