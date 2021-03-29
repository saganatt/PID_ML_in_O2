# Custom cmake config file by jcarius to enable find_package(ONNXRuntime)
# without modifying LIBRARY_PATH and LD_LIBRARY_PATH
# From: https://stackoverflow.com/a/66494534
#
# This will define the following variables:
#   ONNXRuntime_FOUND        -- True if the system has the onnxruntime library
#   ONNXRuntime_INCLUDE_DIRS -- The include directories for onnxruntime
#   ONNXRuntime_LIBRARIES    -- Libraries to link against
#   ONNXRuntime_CXX_FLAGS    -- Additional (required) compiler flags

include(FindPackageHandleStandardArgs)

set(ONNXRuntime_DIR ${CMAKE_CURRENT_LIST_DIR}/onnxruntime-linux-x64-1.7.0)
set(ONNXRuntime_exp_DIR ${CMAKE_CURRENT_LIST_DIR}/onnxruntime-experimental)
set(ONNXRuntime_INCLUDE_DIRS ${ONNXRuntime_DIR}/include ${ONNXRuntime_exp_DIR})
set(ONNXRuntime_CXX_FLAGS "") # no flags needed

find_library(ONNXRuntime_LIBRARY onnxruntime
    PATHS ${ONNXRuntime_DIR}/lib
)

add_library(ONNXRuntime::ONNXRuntime SHARED IMPORTED)
set_property(TARGET ONNXRuntime::ONNXRuntime PROPERTY IMPORTED_LOCATION "${ONNXRuntime_LIBRARY}")
set_property(TARGET ONNXRuntime::ONNXRuntime PROPERTY INTERFACE_INCLUDE_DIRECTORIES "${ONNXRuntime_INCLUDE_DIRS}")
set_property(TARGET ONNXRuntime::ONNXRuntime PROPERTY INTERFACE_COMPILE_OPTIONS "${ONNXRuntime_CXX_FLAGS}")

find_package_handle_standard_args(ONNXRuntime::ONNXRuntime DEFAULT_MSG ONNXRuntime_LIBRARY ONNXRuntime_INCLUDE_DIRS)
