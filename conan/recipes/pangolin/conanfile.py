from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps, cmake_layout
from conan.tools.files import get, copy
import os

class PangolinConan(ConanFile):
    name = "pango"
    version = "0.9.3"
    settings = "os", "arch", "compiler", "build_type"

    def requirements(self):
        self.requires("eigen/3.4.0")
        self.requires("glew/2.2.0", transitive_headers=True, transitive_libs=True)
        self.requires("libpng/1.6.40")
        self.requires("libwebp/1.3.2")
        self.requires("opencv/3.4.20")
        self.requires("zlib/1.3.1")
        self.requires("openexr/2.5.7")
        self.requires("zstd/1.5.5")
        self.requires("opengl/system")
        self.requires("libepoxy/1.5.10")
        self.requires("ffmpeg/6.1", transitive_headers=True, transitive_libs=True)
        self.requires("libjpeg/9e")
        self.requires("libtiff/4.6.0")

    def source(self):
        get(self, f"https://github.com/stevenlovegrove/Pangolin/archive/refs/tags/v{self.version}.tar.gz", strip_root=True)

    def layout(self):
        cmake_layout(self)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["BUILD_EXAMPLES"] = False
        tc.variables["BUILD_TOOLS"] = False

        tc.generate()

        cd = CMakeDeps(self)
        cd.set_property("ffmpeg", "cmake_file_name", "FFMPEG")
        cd.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.components["pangolin"].libs = [
            "pango_core", "pango_display", "pango_geometry",
            "pango_glgeometry", "pango_image", "pango_opengl",
            "pango_packetstream", "pango_plot", "pango_python",
            "pango_scene", "pango_tools", "pango_vars",
            "pango_video", "pango_windowing"
        ]
        self.cpp_info.components["pangolin"].requires = [
            "glew::glew",
            "libjpeg::libjpeg",
            "libpng::libpng",
            "libtiff::libtiff",
            "openexr::openexr",
            "opencv::opencv",
            "eigen::eigen",
            "libwebp::libwebp",
            "zlib::zlib",
            "zstd::zstd",
            "opengl::opengl",
            "libepoxy::libepoxy",
            "ffmpeg::ffmpeg"
        ]
