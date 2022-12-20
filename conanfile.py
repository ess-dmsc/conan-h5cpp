import os
import shutil
from conans import ConanFile, CMake, tools
from conans.util import files


class H5cppConan(ConanFile):
    commit = "95f0e70"

    name = "h5cpp"
    version = commit
    license = "LGPL 2.1"
    url = "https://github.com/ess-dmsc/h5cpp"
    description = "h5cpp wrapper"
    settings = "os", "compiler", "build_type", "arch"
    requires = (
        "hdf5/1.12.2"
    )
    options = {
        "parallel": [True, False],
        "with_boost": [True, False]
    }

    # The temporary build diirectory
    build_dir = f"./{name}/build"

    default_options = (
        "parallel=False",
        "with_boost=False",
        "boost_filesystem:shared=True",
        "boost_system:shared=True",
        "hdf5:enable_cxx=False",
        "hdf5:szip_support=with_libaec",
        "hdf5:szip_encoding=True"
    )
    generators = "cmake"

    def source(self):
        self.source_git(self.commit)

    def source_git(self, commit):
        self.run("git clone https://github.com/ess-dmsc/h5cpp.git")
        self.run("cd h5cpp && git checkout {}".format(commit))

    def requirements(self):
        if self.options.parallel:
            self.options['hdf5'].parallel = True
        else:
            self.options['hdf5'].parallel = False

        if self.options.with_boost:
            self.requires("cmake_findboost_modular/1.69.0@bincrafters/stable")
            self.requires("boost_filesystem/1.69.0@bincrafters/stable")

    def build(self):
        files.mkdir(self.build_dir)
        dest_file = f"{self.build_dir}/conanbuildinfo.cmake"
        shutil.copyfile(
            "conanbuildinfo.cmake",
            dest_file
        )
        with tools.chdir(self.build_dir):
            cmake = CMake(self)
            cmake.definitions["CMAKE_INSTALL_PREFIX"] = ""
            cmake.definitions["CONAN"] = "MANUAL"
            cmake.definitions["H5CPP_DISABLE_TESTS"] = "ON"

            if self.options.with_boost:
                cmake.definitions["H5CPP_WITH_BOOST"] = "ON"
            else:
                cmake.definitions["H5CPP_WITH_BOOST"] = "OFF"

            if self.options.parallel:
                cmake.definitions["WITH_MPI"] = "ON"

            if tools.os_info.is_macos:
                cmake.definitions["CMAKE_MACOSX_RPATH"] = "ON"
                cmake.definitions["CMAKE_SHARED_LINKER_FLAGS"] = "-headerpad_max_install_names"

            self.run(f"cmake --debug-output .. {cmake.command_line}")
            if tools.os_info.is_windows:
                cmake.build(build_dir=".")
            else:
                # DESTDIR is not recommended for Windows
                cmake.build(build_dir=".", target="install", args=["--", "DESTDIR=./install"])

            os.rename(
                "../LICENSE",
                "../LICENSE.h5cpp"
            )

    def package(self):
        folder_name = "h5cpp"

        # Copy headers
        src_path = os.path.join(folder_name, "src")
        self.copy(pattern="*.hpp", dst="include", src=src_path, keep_path=True)

        if tools.os_info.is_windows:
            self.copy(pattern="*.dll", dst="bin", keep_path=False)
            self.copy(pattern="*.lib", dst="lib", keep_path=False)
        else:
            self.copy(pattern="*.a", src=self.build_dir+"/install", keep_path=True)
            self.copy(pattern="*.so*", src=self.build_dir+"/install", keep_path=True)
            self.copy(pattern="*.cmake", src=self.build_dir+"/install", keep_path=True)
            self.copy(pattern="*.dylib*", dst="lib", src=self.build_dir+"/install", keep_path=False)
            self.copy(pattern="*.pdb", dst="bin", src=self.build_dir+"/install", keep_path=False)

        # Copy license
        self.copy("LICENSE.*", src=folder_name)

    def package_info(self):
        self.cpp_info.libs = ["h5cpp"]
