set(BUILD_PANGOLIN_PYTHON OFF)
set(BUILD_EXAMPLES OFF)
set(BUILD_TOOLS OFF)
set(BUILD_TESTS OFF)
set(BUILD_SHARED_LIBS OFF)
set(PANGOLIN_INSTALL OFF)

# Pangolin's optional image codecs and ffmpeg video driver use find_package()
# and then read <Pkg>_LIBRARY / <Pkg>_INCLUDE_DIR. With the Conan toolchain
# (CMAKE_FIND_PACKAGE_PREFER_CONFIG) they find Conan's packages (OpenCV's
# libpng, libjpeg, libtiff, OpenEXR, ffmpeg) or system CMake configs (zstd),
# which don't set those variables, so the build or link breaks. We only use
# the viewer, so switch them off.
set(BUILD_PANGOLIN_LIBPNG OFF)
set(BUILD_PANGOLIN_LIBJPEG OFF)
set(BUILD_PANGOLIN_LIBTIFF OFF)
set(BUILD_PANGOLIN_LIBOPENEXR OFF)
set(BUILD_PANGOLIN_LZ4 OFF)
set(BUILD_PANGOLIN_ZSTD OFF)
set(BUILD_PANGOLIN_LIBRAW OFF)
set(BUILD_PANGOLIN_FFMPEG OFF)

add_subdirectory(Pangolin)
