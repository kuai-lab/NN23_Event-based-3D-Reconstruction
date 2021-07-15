# Event based 3D Reconstruction

Event based 3D Object Reconstruction 연구 Repository입니다.


## 1. Blender 설치


## 2. Blender에 Vision Blender Addon 추가
- Github : https://github.com/Cartucho/vision_blender

## 3. Obj file 불러오기


## 4. Python script 작성

- 처음 시작 option 설정
```
bpy.context.scene.vision_blender.bool_save_gt_data = True
bpy.context.scene.render.engine = 'CYCLES'
```

- object 마다 pass_index 설정
```
bpy.context.object.pass_index = 1
```

- render 시작 (npz 생성)
```
bpy.ops.render.render()
```

## 5. 
