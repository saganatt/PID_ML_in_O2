# Custom cmake config file by jcarius to enable find_package(onnxruntime)
# without modifying LIBRARY_PATH and LD_LIBRARY_PATH
# From: https://stackoverflow.com/a/66494534
#
# This will define the following variables:
#   onnxruntime_FOUND        -- True if the system has the onnxruntime library
#   onnxruntime_INCLUDE_DIRS -- The include directories for onnxruntime
#   onnxruntime_LIBRARIES    -- Libraries to link against
#   onnxruntime_CXX_FLAGS    -- Additional (required) compiler flags

include(FindPackageHandleStandardArgs)

set(onnxruntime_DIR ${CMAKE_CURRENT_LIST_DIR}/onnxruntime-linux-x64-1.7.0)
set(onnxruntime_exp_DIR ${CMAKE_CURRENT_LIST_DIR}/onnxruntime-experimental)
set(onnxruntime_INCLUDE_DIRS ${onnxruntime_DIR}/include ${onnxruntime_exp_DIR})
set(onnxruntime_LIBRARIES onnxruntime)
set(onnxruntime_CXX_FLAGS "") # no flags needed

find_library(onnxruntime_LIBRARY onnxruntime
    PATHS ${onnxruntime_DIR}/lib
)

add_library(onnxruntime SHARED IMPORTED)
set_property(TARGET onnxruntime PROPERTY IMPORTED_LOCATION "${onnxruntime_LIBRARY}")
set_property(TARGET onnxruntime PROPERTY INTERFACE_INCLUDE_DIRECTORIES "${onnxruntime_INCLUDE_DIRS}")
set_property(TARGET onnxruntime PROPERTY INTERFACE_COMPILE_OPTIONS "${onnxruntime_CXX_FLAGS}")

find_package_handle_standard_args(onnxruntime DEFAULT_MSG onnxruntime_LIBRARY onnxruntime_INCLUDE_DIRS)
