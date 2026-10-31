cmake_minimum_required(VERSION 3.23)
# The Conan toolchain is passed by the conan-release preset
# (CMAKE_TOOLCHAIN_FILE), so it applies before project() and to every
# subdirectory, including extern/.
project(SLAMBot)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

option(SLAMBOT_BUILD_EXPERIMENTS "Build book exercises and demos" ON)

# Enable testing at the top level, so ctest finds the tests from the build root.
include(CTest)

add_subdirectory(extern)
add_subdirectory(SLAMBot)

if(SLAMBOT_BUILD_EXPERIMENTS)
    add_subdirectory(experiments)
endif()
