cmake_minimum_required(VERSION 3.10)
project(SLAMBot)

add_subdirectory(extern)

# Conan setup
include(${CMAKE_BINARY_DIR}/../conan/conan_toolchain.cmake)
add_subdirectory(SLAMBot)
