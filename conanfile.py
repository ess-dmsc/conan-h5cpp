import os
from conan import ConanFile, tools
from conan.tools.files import copy, get
from conan.tools.cmake import CMake
from conan.tools.env import VirtualBuildEnv, VirtualRunEnv

class H5CppConan(ConanFile):
    name = "h5cpp"
    version = "0.7.1"
    license = "LGPL-2.1"
    url = "https://github.com/ess-dmsc/h5cpp"
    description = "C++ wrapper for the HDF5 C-library"
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "with_mpi": [True, False],
        "with_boost": [True, False],
        "install_prefix": [None, "ANY"]
    }
    default_options = {
        "shared": True,
        "fPIC": True,
        "with_mpi": False,
        "with_boost": False,
        "hdf5/*:hl": True,
        "hdf5/*:enable_cxx": False,
        "hdf5/*:shared": True,
        "install_prefix": None
    }
    generators = "CMakeToolchain", "CMakeDeps"

    def configure(self):
        if self.options.get_safe("with_mpi", False):
            self.options["hdf5"].parallel = True

    def build_requirements(self):
        self.build_requires("catch2/3.3.2")
        self.build_requires("ninja/1.12.1")
        self.build_requires("zlib/1.3.1")
        if self.settings.os == "Windows":
            self.tool_requires("b2/5.2.1")

    def requirements(self):
        self.requires("hdf5/1.14.5")
        self.requires("catch2/3.3.2")
        self.requires("zlib/1.3.1")
        self.requires("szip/2.1.1")
        self.requires("bzip2/1.0.8")
        if self.options.with_boost:
            self.requires("boost/1.86.0")
        if self.options.with_mpi:
            self.requires("openmpi/4.1.0")

    def source(self):
        data = self.conan_data["sources"][self.version]
        get(self, **data, strip_root=True)

    def build(self):
        cmake = CMake(self)
        build_env = VirtualBuildEnv(self).vars()
        run_env = VirtualRunEnv(self).vars()
        with build_env.apply(), run_env.apply():
            variables = {
                "H5CPP_CONAN": "MANUAL",
                "H5CPP_WITH_MPI": self.options.with_mpi,
                "H5CPP_WITH_BOOST": self.options.with_boost
            }
            if self.options.install_prefix:
                variables["CMAKE_INSTALL_PREFIX"] = self.options.install_prefix

            cmake.configure(variables=variables)
            cmake.build()
            cmake.install()

    def package(self):
        cmake = CMake(self)
        cmake.install()
        copy(self, "LICENSE*", self.source_folder, os.path.join(self.package_folder, "licenses"), keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["h5cpp"]
