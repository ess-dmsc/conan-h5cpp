import os
import shutil
from conans import ConanFile, CMake, tools
from conans.util import files

def source_release(version, sha_string):
    archive_name = "h5cpp.tar.gz"
    tools.download(
        "https://github.com/ess-dmsc/h5cpp/archive/v%s.tar.gz" % version,
        archive_name
    )
    tools.check_sha256(
        archive_name,
        sha_string
    )
    tools.unzip(archive_name)
    os.remove(archive_name)

class H5cppConan(ConanFile):
    package_type = "release"
    # Release (stable) pacakge
    version_number = "0.4.0"
    version = version_number + "-dm2"
    archive_sha256 = "333cd97308dcf969a98308c296ab206cb1958dee298e456a72ce078c4fd65470"
    
    # Test package
    commit = "dc5aeda"

    name = "h5cpp"
    folder_name = "h5cpp-{}".format(version_number)
    if package_type == "test":
        version = commit
        folder_name = name
    license = "LGPL 2.1"
    url = "https://github.com/ess-dmsc/h5cpp"
    description = "h5cpp wrapper"
    settings = "os", "compiler", "build_type", "arch"
    requires = (
        "hdf5/1.10.5-dm3@ess-dmsc/stable"
    )
    options = {
        "parallel": [True, False],
        "with_boost": [True, False]
    }
    
    # The temporary build diirectory
    build_dir = "./%s/build" % folder_name

    default_options = (
        "parallel=False",
        "with_boost=False",
        "boost_filesystem:shared=True",
        "boost_system:shared=True",
        "hdf5:shared=True",
        "hdf5:cxx=False"
    )
    generators = "cmake"
    
    def source(self):
        if self.package_type == "release":
            source_release(self.version_number, self.archive_sha256)
        elif self.package_type == "test":
            self.source_git(self.commit)
            self.folder_name = "h5cpp"
        else:
            raise ConanInvalidConfiguration("Unknown package type: {}".format(self.package_type))
    
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
            cmake.definitions["DISABLE_TESTS"] = "ON"
            
            if self.options.with_boost:
                cmake.definitions["WITH_BOOST"] = "ON"
            else:
                cmake.definitions["WITH_BOOST"] = "OFF"

            if self.options.parallel:
                cmake.definitions["WITH_MPI"] = "ON"

            if tools.os_info.is_macos:
                cmake.definitions["CMAKE_MACOSX_RPATH"] = "ON"
                cmake.definitions["CMAKE_SHARED_LINKER_FLAGS"] = "-headerpad_max_install_names"

            # cmake.configure(source_dir="..", build_dir=".")
            self.run("cmake --debug-output %s %s" % ("..", cmake.command_line))
            if tools.os_info.is_windows:
                cmake.build(build_dir=".")
            else:
                # DESTDIR is not recommended for Windows
                cmake.build(build_dir=".",target="install",args=["--","DESTDIR=./install"])

            os.rename(
                "../LICENSE",
                "../LICENSE.h5cpp"
            )

    def package(self):
        # Copy headers
        src_path = os.path.join(self.folder_name, "src")
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
        self.copy("LICENSE.*", src=self.folder_name)

    def package_info(self):
        self.cpp_info.libs = ["h5cpp"]
