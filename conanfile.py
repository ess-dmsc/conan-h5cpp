from conans import ConanFile, CMake, tools


class H5cppConan(ConanFile):
    """Conan recipe for *h5cpp* """

    name            = "h5cpp"
    version         = "0.6.2"
    license         = "LGPL-2.1-or-later"
    url             = "https://github.com/ess-dmsc/h5cpp"
    description     = "Cpp wrapper for the HDF5 C API"

    revision_mode   = "scm"

    settings        = "os", "compiler", "build_type", "arch"
    options         = {"with_boost": [True, False]}
    default_options = {
        "with_boost": False,
        # propagated options for dependencies
        "hdf5:enable_cxx": False,
        "hdf5:szip_support": "with_libaec",
        "hdf5:szip_encoding": True,
    }

    generators      = "cmake", "cmake_find_package"
    no_copy_source  = True

    _source_subfolder = "source"

    def source(self):
        data = self.conan_data["sources"][self.version]
        repo = tools.Git(folder=self._source_subfolder)
        repo.clone(data["url"], "master")
        with tools.chdir(self._source_subfolder):
            self.run(f"git checkout {data['commit']}")

    def requirements(self):
        self.requires("hdf5/1.14.1")
        if self.options.with_boost:
            self.requires("boost/1.81.0")
            self.requires("zlib/1.2.13")

    def _configure_cmake(self):
        if hasattr(self, "_cmake"):
            return self._cmake

        cmake = CMake(self)
        cmake.definitions.update({
            "CMAKE_INSTALL_PREFIX": self.package_folder.replace("\\", "/"),
            "H5CPP_DISABLE_TESTS": "ON",
            "H5CPP_WITH_BOOST": "ON" if self.options.with_boost else "OFF",
        })
        cmake.configure(source_folder=self._source_subfolder)
        self._cmake = cmake
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()
        cmake.install()

    def package(self):
        # Install step already populated *self.package_folder*; just copy licence.
        self.copy("LICENSE*", dst="licenses", src=self._source_subfolder)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
