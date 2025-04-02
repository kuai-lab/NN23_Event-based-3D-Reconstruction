# Event based 3D Reconstruction

Repository of Event-based 3D Object Reconstruction 
![image](https://user-images.githubusercontent.com/44921488/125921177-210e8939-f4f0-467a-8e05-812a64d8aed1.png)

# Optical Flow & Depth Map GT
## 1. requirements
### Blender Install
- https://www.blender.org/

## 2. Adding the Visionon Blender Addon on Blender
- Github: https://github.com/Cartucho/vision_blender

## 3. Reading OBJ file


## 4. Writing Python script
- Initial setup of option Setting
```
bpy.context.scene.vision_blender.bool_save_gt_data = True
bpy.context.scene.render.engine = 'CYCLES'
cam = scene.objects['Camera']
cam.location = (0, 4.0, 0.5) #카메라 초기 위치 설정
```

- Set pass_index for each object
```
bpy.context.object.pass_index = 1
```
- Camera Pose json export

```
frame_data = {
        'file_path': scene.render.filepath,
        'rotation': radians(stepsize),
        'transform_matrix': listify_matrix(cam.matrix_world)
    }
```

- OBJ normalize
```
import bpy

max_dim = 2

context = bpy.context

mesh_obs = (o for o in context.selected_objects 
        if o.type == 'MESH' and o.dimensions.length)

for o in mesh_obs:
    o.scale *= max_dim / max(o.dimensions)
```

- Start rendering (npz generation)
```
bpy.ops.render.render()
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
[Move Folder](https://github.com/kuai-lab/Event-based-3D-Reconstruction/tree/main/mesh2pc)
# Event Signal(v2e)
[Move Folder](https://github.com/kuai-lab/Event-based-3D-Reconstruction/tree/main/v2e)
