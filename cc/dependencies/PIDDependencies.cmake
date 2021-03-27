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

set(CMAKE_MODULE_PATH ${CMAKE_CURRENT_LIST_DIR} ${CMAKE_MODULE_PATH})

# Required packages
#
# Order is not completely irrelevant.
#
# Generally speaking we should prefer the CONFIG variant of the find_package. We
# explicitely don't use the CONFIG variant (i.e. we do use the MODULE variant)
# only for some packages XXX where we define our own FindXXX.cmake module (e.g.
# to complement and/or fix what's done in the package's XXXConfig.cmake file)

# Needed for find_package to work properly
include(ONNXRuntimeConfig)
# include(ONNXRuntimeVersion) # TODO: Check if really needed
find_package(onnxruntime)
set_package_properties(onnxruntime PROPERTIES TYPE REQUIRED)

feature_summary(WHAT ALL FATAL_ON_MISSING_REQUIRED_PACKAGES)
