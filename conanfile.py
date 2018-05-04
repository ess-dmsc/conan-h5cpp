import os
import shutil
from conans import ConanFile, CMake, tools
from conans.util import files


class H5cppConan(ConanFile):
    src_version = "0.0.6"
    version = "0.0.6"
    # SHA256 Checksum for this versioned release (.tar.gz)
    # NOTE: This should be updated every time the version is updated
    archive_sha256 = "e6ca981d9a38f30c07c336da5db43f191bfa05413e583148e11544870a5fd8d0"

    name = "h5cpp"
    license = "LGPL 2.1"
    url = "https://bintray.com/ess-dmsc/h5cpp"
    description = "h5cpp wrapper"
    settings = "os", "compiler", "build_type", "arch"
    build_requires = "cmake_installer/3.10.0@conan/stable"
    requires = (
        "Boost/1.62.0@ess-dmsc/stable",
        "hdf5/1.10.2@dwerder/mpienabled",
        "gtest/3121b20-dm2@ess-dmsc/stable"
    )

    # The folder name when the *.tar.gz release is extracted
    folder_name = "h5cpp-%s" % src_version
    # The name of the archive that is downloaded from Github
    archive_name = "%s.tar.gz" % folder_name
    # The temporary build diirectory
    build_dir = "./%s/build" % folder_name

    options = {
        "parallel": [True, False],
    }
    default_options = (
        "parallel=False",
        "Boost:shared=True",
        "hdf5:shared=True",
        "gtest:shared=True"
    )

    generators = "cmake"

    def requirements(self):
        if self.options.parallel:
            self.requires('mpich/3.2.1@ess-dmsc/stable')

    def source(self):
        tools.download(
            "https://github.com/ess-dmsc/h5cpp/archive/v%s.tar.gz" % self.src_version,
            self.archive_name
        )
        tools.check_sha256(
            self.archive_name,
            self.archive_sha256
        )
        tools.unzip(self.archive_name)
        os.unlink(self.archive_name)

    def build(self):
        # Workaround to find the Conan-installed version of Boost on systems
        # with Boost 1.41 installed.
        tools.replace_in_file(
            "%s/cmake/BoostLibraryConfig.cmake" % self.folder_name,
            "1.41",
            "1.62"
        )

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

            # cmake.configure(source_dir="..", build_dir=".")
            self.run("cmake --debug-output %s %s" % ("..", cmake.command_line))
            cmake.build(build_dir=".")
            os.system("make install DESTDIR=./install")

            os.rename(
                "../LICENSE",
                "../LICENSE.h5cpp"
            )

    def package(self):
        self.copy("*", dst="include", src=self.build_dir+"/install/include")
        self.copy("*", dst="lib", src=self.build_dir+"/install/lib")
        self.copy("*", dst="lib64", src=self.build_dir+"/install/lib64")
        self.copy("LICENSE.*", src=self.folder_name)

    def package_info(self):
        self.cpp_info.libs = ["h5cpp"]
        if tools.os_info.linux_distro == "fedora" or tools.os_info.linux_distro == "centos":
            self.cpp_info.libdirs = ["lib64"]
