cmake_minimum_required(VERSION 3.10)
project(SLAMBot)

# Conan setup
include(${CMAKE_BINARY_DIR}/../conan/conan_toolchain.cmake)

enable_testing()
add_subdirectory(SLAMBot)
