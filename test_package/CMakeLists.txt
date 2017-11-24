project(PackageTest CXX)
cmake_minimum_required(VERSION 2.8.12)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup(SKIP_RPATH)

add_definitions(-std=c++11)

add_executable(example example.cpp)
find_library(H5CPP_LIB h5cpp_shared)
target_link_libraries(example ${H5CPP_LIB})
