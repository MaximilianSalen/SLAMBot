cmake_minimum_required(VERSION 3.23)

# The Conan toolchain is passed by the conan-release preset
# (CMAKE_TOOLCHAIN_FILE), so it applies before project().
project(SLAMBot LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

option(SLAMBOT_BUILD_EXPERIMENTS "Build book exercises and demos" ON)

list(APPEND CMAKE_MODULE_PATH ${PROJECT_SOURCE_DIR}/cmake)
include(Sanitizers)
include(Warnings)
include(SlambotModule)

# Enable testing at the top level, so ctest finds the tests from the build root.
include(CTest)
if(BUILD_TESTING)
    find_package(Catch2 REQUIRED)
    include(Catch)
endif()

add_subdirectory(slambot)
if(SLAMBOT_BUILD_EXPERIMENTS)
    add_subdirectory(experiments)
endif()
