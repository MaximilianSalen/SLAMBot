#############################
# Experiments
#############################
# Book exercises and package demos. They are not part of the slambot library
# and are not registered with CTest. demo_opencv opens a window, so it needs a
# display and must not run in CI.

find_package(Sophus REQUIRED)
find_package(OpenCV REQUIRED)

# Sophus: SO(3) group multiplication.
add_executable(demo_sophus demos/sophus_demo.cpp)
target_link_libraries(demo_sophus PRIVATE
    Sophus::Sophus
)

# OpenCV: show an image in a window.
add_executable(demo_opencv demos/opencv_demo.cpp)
target_link_libraries(demo_opencv PRIVATE
    opencv_core
    opencv_highgui
)

# Book ch7: ORB features. Usage: orb_features <img1> <img2>
add_executable(orb_features ch07_orb/orb_features.cpp)
target_link_libraries(orb_features PRIVATE
    opencv_core
    opencv_imgcodecs
    opencv_features2d
    opencv_highgui
)
