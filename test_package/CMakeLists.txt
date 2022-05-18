project(h5cpp-example LANGUAGES CXX C)
cmake_minimum_required(VERSION 2.8.12)

set(WITH_BOOST OFF CACHE BOOL "Require Boost for filesystem support")
if (WITH_BOOST)
  set(CMAKE_CXX_STANDARD 11)
else()
  set(CMAKE_CXX_STANDARD 17)
endif()

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup(KEEP_RPATHS)

add_executable(example example.cpp)

if (WIN32)
  target_link_libraries(example
  PRIVATE ${CONAN_LIBS})
else()
  find_package(hdf5 REQUIRED)
  find_package(h5cpp REQUIRED)
  target_link_libraries(example
  PRIVATE h5cpp::h5cpp hdf5::hdf5)
endif()
