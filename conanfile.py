import os
import shutil
from conans import ConanFile, CMake, tools
from conans.util import files


class H5cppConan(ConanFile):
    version = "0.0.4"
    # SHA256 Checksum for this versioned release (.tar.gz)
    # NOTE: This should be updated every time the version is updated
    archive_sha256 = "b5786a0531690edb102150357cf57dca2a01653b12677228113ab57a2adb061f"

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

    # The folder name when the *.tar.gz release is extracted
    folder_name = "h5cpp-%s" % version
    # The name of the archive that is downloaded from Github
    archive_name = "%s.tar.gz" % folder_name
    # The temporary build diirectory
    build_dir = "./%s/build" % folder_name

    default_options = (
        "Boost:shared=True",
        "hdf5:shared=True",
        "gtest:shared=True"
    )
    generators = "cmake"

    def source(self):
        tools.download(
            "https://github.com/ess-dmsc/h5cpp/archive/v%s.tar.gz" % self.version,
            self.archive_name
        )
        tools.check_sha256(
            self.archive_name,
            self.archive_sha256
        )
        tools.unzip(self.archive_name)
        os.unlink(self.archive_name)

    def build(self):
        files.mkdir(self.build_dir)
        dest_file = "%s/conanbuildinfo.cmake" % self.build_dir
        shutil.copyfile(
            "conanbuildinfo.cmake",
            dest_file
        )
        with tools.chdir(self.build_dir):
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

#        os.rename(
#            "../LICENSE",
#            "../LICENSE.h5cpp"
#        )

    def package(self):
        self.copy("*", dst="include", src=self.build_dir+"/install/include")
        self.copy("*", dst="lib", src=self.build_dir+"/install/lib")
        self.copy("*", dst="lib64", src=self.build_dir+"/install/lib64")
        self.copy("LICENSE.*", src="h5cpp")

    def package_info(self):
        self.cpp_info.libs = ["h5cpp"]
        if tools.os_info.linux_distro == "fedora" or tools.os_info.linux_distro == "centos":
            self.cpp_info.libdirs = ["lib64"]
