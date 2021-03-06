# Copyright CERN and copyright holders of ALICE O2. This software is distributed
# under the terms of the GNU General Public License v3 (GPL Version 3), copied
# verbatim in the file "COPYING".
#
# See http://alice-o2.web.cern.ch/license for full licensing information.
#
# In applying this license CERN does not waive the privileges and immunities
# granted to it by virtue of its status as an Intergovernmental Organization or
# submit itself to any jurisdiction.

# CMake analog of #pragma once
include_guard()

# set(CMAKE_MODULE_PATH ${CMAKE_CURRENT_LIST_DIR} ${CMAKE_MODULE_PATH})

# Required packages
# Order is not completely irrelevant.

# Needed for find_package to work properly
set(ONNXRuntime\:\:ONNXRuntime_DIR ${CMAKE_CURRENT_LIST_DIR})
include(${ONNXRuntime\:\:ONNXRuntime_DIR}/ONNXRuntimeVersion.cmake)
find_package(ONNXRuntime::ONNXRuntime REQUIRED)
