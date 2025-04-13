cmake_minimum_required(VERSION 3.15)
project(SLAMBot)


# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)


set(CMAKE_GENERATOR "Ninja")

if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release)
endif()


# Find required packes
find_package(Eigen3 REQUIRED)
find_package(OpenCV REQUIRED)


# Include third-party libraries
add_subdirectory(third_party/sophus)
add_subdirectory(third_party/pangolin)
add_subdirectory(third_party/g2o)

# Add include directories
include_directories(
    ${EIGEN3_INCLUDE_DIRS}
    ${OpenCV_INCLUDE_DIRS}
    ${CMAKE_SOURCE_DIR}/include
)            

# Define source files
file(GLOB_RECURSE SOURCES src/*.cpp)

# Add the executable
add_executable(${PROJECT_NAME} ${SOURCES})


# Link libraries
target_link_libraries(
    ${PROJECT_NAME}
    Eigen3::Eigen
    ${OpenCV_LIBS}
    Sophus
    Pangolin
    g2o
)

