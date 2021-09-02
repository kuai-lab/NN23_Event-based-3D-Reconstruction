# Pybind11
### pybind11을 활용시 대략 31.2배 정도 빠른 속도로 point cloud 생성이 가능했다.
---
## Setting
- Pybind11 clone
- build 폴더 생성
- CMakeLists.txt 작성
```Bash
git clone https://github.com/pybind/pybind11
mkdir build
cd build
cmake .. && make
```
### CMakeLists.txt
```Text
cmake_minimum_required(VERSION 3.4) #Version 명시
project(depth_2_pc) # project aud
add_subdirectory(pybind11) # Subdirectory 추가
pybind11_add_module(generate_pointcloud generate_pointcloud.cpp) # C++과 binding할 module 명시
```
---
## generate_pointcloud.cpp 작성

```C++
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <iostream>

namespace py = pybind11;
```
- pybind11.h와 numpy.h를 불러온다.
```C++
py::array_t<double> generate_pointcloud_C(py::array_t<double> depth, py::array_t<double> intrinsic, py::array_t<double> extrinsic, int scalingFactor){
    '''
    '''
}
```
- pybind11에서는 numpy.ndarray를 py::array_t 자료형으로 받을 수있다.
```C++
    // initialize vectors
    // depth.size = 83040 = 240 * 346
    std::vector<double> depth_v(depth.size());
    std::vector<double> intrinsic_v(intrinsic.size());
    std::vector<double> extrinsic_v(extrinsic.size());
    
    //copy py::array -> std::vector
    std::memcpy(depth_v.data(),depth.data(),depth.size()*sizeof(double));
    std::memcpy(intrinsic_v.data(),intrinsic.data(),intrinsic.size()*sizeof(double));
    std::memcpy(extrinsic_v.data(),extrinsic.data(),extrinsic.size()*sizeof(double));
```
- py::array_t로 받아온 numpy data를 c++의 vector로 옮겨준다
- 우선 array_t의 size만큼 vector에 할당한다.
- memcpy를 통해 vector에 numpy array의 data를 옮긴다.
```C++
double focalLengthX = intrinsic_v[0];
    double focalLengthY = intrinsic_v[4];
    double centerX = intrinsic_v[2];
    double centerY = intrinsic_v[5];

    std::vector<double> X;
    std::vector<double> Y;
    std::vector<double> Z;

    int i = 0;
    for (int v = 0 ; v<240; v++){
        for (int u = 0; u<346; u++){
            if (depth_v[346*v+u]<=0){
                i++;
                continue;
            }
            double z = depth_v[346*v+u] / scalingFactor;
            double x = (u - centerX) * z / focalLengthX;
            double y = (v - centerY) * z / focalLengthY;

            

            double temp_x = extrinsic_v[0]*(x - extrinsic_v[3]) + extrinsic_v[4]*(y - extrinsic_v[7]) + extrinsic_v[8] * (z - extrinsic_v[11]);
            double temp_y = extrinsic_v[1]*(x - extrinsic_v[3]) + extrinsic_v[5]*(y - extrinsic_v[7]) + extrinsic_v[9] * (z - extrinsic_v[11]);
            double temp_z = extrinsic_v[2]*(x - extrinsic_v[3]) + extrinsic_v[6]*(y - extrinsic_v[7]) + extrinsic_v[10] *(z - extrinsic_v[11]);

            X.push_back(temp_x);
            Y.push_back(temp_y);
            Z.push_back(temp_z);
        }
    }
    X.insert(X.end(), Y.begin(), Y.end());
    X.insert(X.end(), Z.begin(), Z.end());
```
- 가져온 depth, intrinsic, extrinsic 값들로 부터 PointCloud 좌표를 뽑는다.
- 나온 값들은 vector X에 모아준다.
```C++
    // allocate py::array (to pass the result of the C++ function to Python)
    auto result        = py::array_t<double>(X.size());
    auto result_buffer = result.request();
    int *result_ptr    = (int *) result_buffer.ptr;

    // copy std::vector -> py::array
    std::memcpy(result_ptr,X.data(),X.size()*sizeof(double));

    return result;
```
- 다시 vector자료형을 다시 numpy 자료형으로 바꾸어 return 해준다.
```C++
PYBIND11_MODULE(generate_pointcloud, handle){
    handle.doc() = "d2pc util c++ binding";
    handle.def("generate_pointcloud_C", &generate_pointcloud_C);
}
```
- .doc() 는 모듈의 설명을 담는다
- .def() 는 python으로 내보낼 함수와 설명을 담는다.
---
## python에서 import
```python
from build.generate_pointcloud import *
```
- import후 파이썬 기존 함수처럼 활용할 수 있다.
---
## 속도 비교
총 100개의 depth data(.npz) 로 부터 Point cloud를 생성
### generate_pointcloud_C (pybind11 바인딩)
```
Generate point cloud with 100 input depth maps.
100%|████████████████████████████████████████| 100/100 [00:00<00:00, 445.68it/s]
---0.2268059253692627s seconds---
Point cloud generated
```
### generate_pointcloud (python 코드)
```
Generate point cloud with 100 input depth maps.
100%|█████████████████████████████████████████| 100/100 [00:07<00:00, 14.10it/s]
---7.09568452835083s seconds---
Point cloud generated
```