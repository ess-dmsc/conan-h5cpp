import os
import shutil
from conans import ConanFile, CMake, tools
from conans.util import files


class H5cppConan(ConanFile):
    name = "h5cpp"
    version = "fe52beb"
    license = "BSD 2-Clause"
    url = "https://bintray.com/ess-dmsc/h5cpp"
    settings = "os", "compiler", "build_type", "arch"
    requires = (
        "Boost/1.62.0@ess-dmsc/stable",
        "hdf5/1.10.1-dm1@ess-dmsc/stable",
        "gtest/3121b20-dm1@ess-dmsc/testing"
    )
    build_requires = "cmake_installer/1.0@conan/stable"
    default_options = (
        "Boost:shared=True",
        "hdf5:shared=True",
        "gtest:shared=True",
        "cmake_installer:version=3.9.0"
    )
    generators = "cmake"

    def source(self):
        self.run("git clone -b master --single-branch https://github.com/ess-dmsc/h5cpp.git")
        self.run("cd h5cpp && git checkout fe52bebe31fcca001b23c67b0e73043fe513691e")

    def build(self):
        files.mkdir("./h5cpp/build")
        shutil.copyfile(
            "conanbuildinfo.cmake",
            "./h5cpp/build/conanbuildinfo.cmake"
        )
        with tools.chdir("./h5cpp/build"):
            cmake = CMake(self)
            cmake.definitions["CMAKE_INSTALL_PREFIX"] = ""

            if tools.os_info.is_macos:
                cmake.definitions["CMAKE_MACOSX_RPATH"] = "ON"
                cmake.definitions["CMAKE_SHARED_LINKER_FLAGS"] = "-headerpad_max_install_names"

            cmake.configure(source_dir="..", build_dir=".")
            cmake.build(build_dir=".")
            os.system("make install DESTDIR=./install")

            if tools.os_info.is_macos:
                os.system("install_name_tool -id '@rpath/libh5cpp_shared.dylib' "
                          "h5cpp/libh5cpp_shared.dylib")

        os.rename(
            "h5cpp/LICENSE",
            "h5cpp/LICENSE.h5cpp"
        )

    def package(self):
        self.copy("*.hpp", dst="include", src="h5cpp/build/install")
        if self.settings.os == "Macos":
            self.copy("*.dylib*", dst="lib", src="h5cpp/build/install", keep_path=False)
        else:
            self.copy("*.so*", dst="lib", src="h5cpp/build/install", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)
        self.copy("LICENSE.*", src="h5cpp")

    def package_info(self):
        self.cpp_info.libs = ["h5cpp_shared"]
