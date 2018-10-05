project(h5cpp-example LANGUAGES CXX C)
cmake_minimum_required(VERSION 2.8.12)
set(CMAKE_CXX_STANDARD 11)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup(KEEP_RPATHS)

find_package(Boost COMPONENTS filesystem system REQUIRED)
find_package(h5cpp REQUIRED)

add_executable(example example.cpp)
target_link_libraries(example
  PRIVATE h5cpp)
