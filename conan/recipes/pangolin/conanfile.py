from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps, cmake_layout
from conan.tools.files import get, copy
import os

class PangolinConan(ConanFile):
    name = "pangolin"
    version = "0.9.3"
    settings = "os", "arch", "compiler", "build_type"

    def requirements(self):
        self.requires("eigen/3.4.0")
        self.requires("glew/2.2.0", transitive_headers=True, transitive_libs=True)
        self.requires("libpng/1.6.40")
        self.requires("libwebp/1.3.2", override=True)
        self.requires("opencv/3.4.20")
        self.requires("zlib/1.3.1")
        self.requires("openexr/2.5.7")
        self.requires("zstd/1.5.5")
        self.requires("opengl/system")
        self.requires("libepoxy/1.5.10")
        self.requires("ffmpeg/6.1", transitive_headers=True, transitive_libs=True)
        self.requires("libjpeg/9e")

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
        cd.set_property("libpng", "cmake_file_name", "PNG")
        cd.set_property("libjpeg", "cmake_file_name", "JPEG")
        cd.set_property("zstd", "cmake_file_name", "ZSTD")
        cd.set_property("openexr", "cmake_file_name", "OpenEXR")
        cd.set_property("libtiff", "cmake_file_name", "TIFF")
        cd.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["pangolin"]
