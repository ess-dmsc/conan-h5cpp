import os
import shutil
from conans import ConanFile, CMake, tools
from conans.util import files


class H5cppConan(ConanFile):
    version = "0.0.4"
    # SHA256 Checksum for this versioned release (.tar.gz)
    # NOTE: This should be updated every time the version is updated
    #archive_sha256 = "c45029c0a0f1a88d416af143e34de96b3091642722aa2d8c090916c6d1498c2e"

    name = "h5cpp"
    license = "LGPL 2.1"
    url = "https://bintray.com/ess-dmsc/h5cpp"
    description = "h5cpp wrapper"
    settings = "os", "compiler", "build_type", "arch"
    requires = (
        "Boost/1.62.0@ess-dmsc/stable",
        "hdf5/1.10.1-dm3@ess-dmsc/stable",
        "gtest/3121b20-dm2@ess-dmsc/stable"
    )

    default_options = (
        "Boost:shared=True",
        "hdf5:shared=True",
        "gtest:shared=True"
    )
    generators = "cmake"

    def source(self):
        self.run("git clone -b master --single-branch https://github.com/ess-dmsc/h5cpp.git")

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
                os.system("install_name_tool -id '@rpath/libh5cpp.dylib' "
                          "h5cpp/libh5cpp.dylib")

        os.rename(
            "h5cpp/LICENSE",
            "h5cpp/LICENSE.h5cpp"
        )

    def package(self):
        self.copy("*", dst="include", src="h5cpp/build/install/include")
        self.copy("*", dst="lib", src="h5cpp/build/install/lib")
        self.copy("*", dst="lib64", src="h5cpp/build/install/lib64")
        self.copy("LICENSE.*", src="h5cpp")

    def package_info(self):
        self.cpp_info.libs = ["h5cpp"]
        if tools.os_info.linux_distro == "fedora" or tools.os_info.linux_distro == "centos":
            self.cpp_info.libdirs = ["lib64"]
