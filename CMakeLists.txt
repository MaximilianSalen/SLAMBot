cmake_minimum_required(VERSION 3.10)
project(SLAMBot)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

add_subdirectory(extern)

# Conan setup
include(${CMAKE_BINARY_DIR}/../conan/conan_toolchain.cmake)
add_subdirectory(SLAMBot)
