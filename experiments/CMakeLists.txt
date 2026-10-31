#############################
# Experiments
#############################
# Book exercises and package demos. They are not part of the SLAMBot library
# and are not registered with CTest. The demo_opencv and demo_pangolin targets
# open windows, so they need a display and must not run in CI.

find_package(Sophus REQUIRED)
# No target here uses xkbcommon directly; OpenCV's highgui (Wayland) needs it.
# Pangolin's pkg_check_modules(xkbcommon ...) caches xkbcommon_FOUND, so
# Conan's OpenCVConfig skips find_dependency(xkbcommon) and the target
# xkbcommon::libxkbcommon would be missing. Find it explicitly first.
find_package(xkbcommon REQUIRED)
find_package(OpenCV REQUIRED)

# Sophus: SO(3) group multiplication.
add_executable(demo_sophus TestSophus.cpp)
target_link_libraries(demo_sophus PRIVATE
    Sophus::Sophus
)

# OpenCV: show an image in a window.
add_executable(demo_opencv TestOpenCV.cpp)
target_link_libraries(demo_opencv PRIVATE
    opencv_core
    opencv_highgui
)

# Pangolin (extern/): 3D viewer with a UI panel.
add_executable(demo_pangolin TestPangolin.cpp)
target_link_libraries(demo_pangolin PRIVATE
    pango_display
)

# Book ch7: ORB features. Usage: orb_features <img1> <img2>
add_executable(orb_features FeatureExtraction.cpp)
target_link_libraries(orb_features PRIVATE
    opencv_core
    opencv_imgcodecs
    opencv_features2d
    opencv_highgui
)
