project(h5cpp-example LANGUAGES CXX C)
cmake_minimum_required(VERSION 2.8.12)
set(CMAKE_CXX_STANDARD 11)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup(SKIP_RPATH)

find_package(h5cpp REQUIRED)

find_library(H5CPP_LIB h5cpp)
target_link_libraries(example ${H5CPP_LIB})

#add_executable(example example.cpp)
#target_link_libraries(example h5cpp_shared)
