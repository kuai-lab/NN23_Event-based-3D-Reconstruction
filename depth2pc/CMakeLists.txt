cmake_minimum_required(VERSION 3.4)
project(depth_2_pc)
add_subdirectory(pybind11)
pybind11_add_module(generate_pointcloud generate_pointcloud.cpp)