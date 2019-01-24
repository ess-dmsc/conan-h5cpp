import os
import shutil
from conans import ConanFile, CMake, tools
from conans.util import files


class H5cppConan(ConanFile):
    src_version = "0.1.0"
    version = "0.1.0-dm2"
    # SHA256 Checksum for this versioned release (.tar.gz)
    # NOTE: This should be updated every time the version is updated
    archive_sha256 = "c811b8954bad344e8fe62b830cc04685d21e340a6a1dcbe557f0cdd03414a7f8"

    name = "h5cpp"
    license = "LGPL 2.1"
    url = "https://bintray.com/ess-dmsc/h5cpp"
    description = "h5cpp wrapper"
    settings = "os", "compiler", "build_type", "arch"
    build_requires = "cmake_installer/3.10.0@conan/stable"
    requires = (
        "cmake_findboost_modular/1.65.1@bincrafters/stable",
        "boost_filesystem/1.65.1@bincrafters/stable",
        "boost_system/1.65.1@bincrafters/stable",
        "hdf5/1.10.2-dm2@ess-dmsc/stable"
    )
    options = {
        "parallel": [True, False]
    }

    # The folder name when the *.tar.gz release is extracted
    folder_name = "h5cpp-%s" % src_version
    # The name of the archive that is downloaded from Github
    archive_name = "%s.tar.gz" % folder_name
    # The temporary build diirectory
    build_dir = "./%s/build" % folder_name

    default_options = (
        "parallel=False",
        "boost_filesystem:shared=True",
        "boost_system:shared=True",
        "hdf5:shared=True",
        "hdf5:cxx=False",
        "gtest:shared=True"
    )
    generators = "cmake"

    def requirements(self):
        if self.options.parallel:
            self.options['hdf5'].parallel = True
        else:
            self.options['hdf5'].parallel = False

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
            "1.65"
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
            cmake.definitions["CONAN"] = "MANUAL"

            if self.options.parallel:
                cmake.definitions["WITH_MPI"] = "ON"

            if tools.os_info.is_macos:
                cmake.definitions["CMAKE_MACOSX_RPATH"] = "ON"
                cmake.definitions["CMAKE_SHARED_LINKER_FLAGS"] = "-headerpad_max_install_names"

            # cmake.configure(source_dir="..", build_dir=".")
            self.run("cmake --debug-output %s %s" % ("..", cmake.command_line))
            cmake.build(build_dir=".")
            cmake.build(build_dir=".",target="install",args=["--","DESTDIR=./install"])

            os.rename(
                "../LICENSE",
                "../LICENSE.h5cpp"
            )

    def package(self):
        # Copy headers
        src_path = os.path.join(self.folder_name, "src")
        self.copy(pattern="*.hpp", dst="include", src=src_path, keep_path=True)

        # Copy libs
        self.copy(pattern="*.a", src=self.build_dir+"/install", keep_path=True)
        self.copy(pattern="*.so*", src=self.build_dir+"/install", keep_path=True)
        self.copy(pattern="*.cmake", src=self.build_dir+"/install", keep_path=True)
        self.copy(pattern="*.lib", dst="lib", src=self.build_dir+"/install", keep_path=False)
        self.copy(pattern="., *.dll", dst="bin", src=self.build_dir+"/install", keep_path=False)
        self.copy(pattern="*.dylib*", dst="lib", src=self.build_dir+"/install", keep_path=False)
        self.copy(pattern="*.pdb", dst="bin", src=self.build_dir+"/install", keep_path=False)

        # Copy license
        self.copy("LICENSE.*", src=self.folder_name)

    def package_info(self):
        self.cpp_info.libs = ["h5cpp"]
