#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <iostream>

namespace py = pybind11;

py::array_t<double> generate_pointcloud_C(py::array_t<double> depth, py::array_t<double> intrinsic, py::array_t<double> extrinsic, int scalingFactor){
    // initialize vectors
    // depth.size = 83040 = 240 * 346

    std::vector<double> depth_v(depth.size());
    std::vector<double> intrinsic_v(intrinsic.size());
    std::vector<double> extrinsic_v(extrinsic.size());
    
    //copy py::array -> std::vector
    std::memcpy(depth_v.data(),depth.data(),depth.size()*sizeof(double));
    std::memcpy(intrinsic_v.data(),intrinsic.data(),intrinsic.size()*sizeof(double));
    std::memcpy(extrinsic_v.data(),extrinsic.data(),extrinsic.size()*sizeof(double));

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

    
    // allocate py::array (to pass the result of the C++ function to Python)
    auto result        = py::array_t<double>(X.size());
    auto result_buffer = result.request();
    int *result_ptr    = (int *) result_buffer.ptr;

    // copy std::vector -> py::array
    std::memcpy(result_ptr,X.data(),X.size()*sizeof(double));

    return result;
}

PYBIND11_MODULE(generate_pointcloud, handle){
    handle.doc() = "d2pc util c++ binding";
    handle.def("generate_pointcloud_C", &generate_pointcloud_C);
}