# Adjusted from the O2 CMakeLists.txt

# Copyright CERN and copyright holders of ALICE O2. This software is distributed
# under the terms of the GNU General Public License v3 (GPL Version 3), copied
# verbatim in the file "COPYING".
#
# See http://alice-o2.web.cern.ch/license for full licensing information.
#
# In applying this license CERN does not waive the privileges and immunities
# granted to it by virtue of its status as an Intergovernmental Organization or
# submit itself to any jurisdiction.

# Preamble

cmake_minimum_required(VERSION 3.17 FATAL_ERROR)

# it's important to specify accurately the list of languages. for instance C and
# C++ as we _do_ have some C files to compile explicitely as C (e.g. gl3w.c)
project(PID LANGUAGES C CXX VERSION 1.2.0)

# Project wide setup

set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} ${CMAKE_CURRENT_SOURCE_DIR}/cmake)
set_property(GLOBAL PROPERTY REPORT_UNDEFINED_PROPERTIES)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED TRUE)

# External dependencies
include(dependencies/CMakeLists.txt)
