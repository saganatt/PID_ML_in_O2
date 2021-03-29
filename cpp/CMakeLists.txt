cmake_minimum_required(VERSION 3.17 FATAL_ERROR)

project(PID LANGUAGES CXX VERSION 1.0.0)

# Project wide setup
set_property(GLOBAL PROPERTY REPORT_UNDEFINED_PROPERTIES)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED TRUE)

# External dependencies
include(dependencies/CMakeLists.txt)

# Project files
add_executable(pid-in-cpp
               model-explorer.cpp)

# include_directories(_)

target_link_libraries(pid-in-cpp ONNXRuntime::ONNXRuntime)
