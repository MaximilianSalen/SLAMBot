set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find Eigen
find_package(Eigen3 REQUIRED)

add_executable(SLAMBot main.cpp)

# Link Eigen
target_link_libraries(SLAMBot PRIVATE Eigen3::Eigen)
