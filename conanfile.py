import os
from conans import ConanFile, CMake, tools
from conans.errors import ConanException


class H5cppConan(ConanFile):
    name = "h5cpp"
    version = "<version>"
    license = "BSD 2-Clause"
    url = "https://bintray.com/ess-dmsc/h5cpp"
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake", "virtualrunenv"

    def source(self):
        self.run("git clone https://github.com/ess-dmsc/h5cpp.git")
        self.run("cd h5cpp && git checkout <commit>")

    def build(self):
        cmake = CMake(self)

        try:
            self.output.info("Try to run cmake3")
            self.run("cmake3 --version")
            cmake_command = "cmake3"
        except ConanException:
            self.output.info("Using cmake instead of cmake3")
            cmake_command = "cmake"

        cmake.definitions["BUILD_EVERYTHING"] = "OFF"
        if tools.os_info.is_macos:
            cmake.definitions["CMAKE_MACOSX_RPATH"] = "ON"
            cmake.definitions["CMAKE_SHARED_LINKER_FLAGS"] = "-headerpad_max_install_names"

        self.run('%s h5cpp %s' % (cmake_command, cmake.command_line))
        self.run("%s --build . %s" % (cmake_command, cmake.build_config))

        if tools.os_info.is_macos:
            os.system("install_name_tool -id '@rpath/libh5cpp_shared.dylib' "
                      "h5cpp/libh5cpp_shared.dylib")

        os.rename(
            "h5cpp/LICENSE",
            "h5cpp/LICENSE.h5cpp"
        )

    def package(self):
        self.copy("*.hpp", dst="include/h5cpp", src="h5cpp/src/include/h5cpp")
        if self.settings.os == "Macos":
            self.copy("*.dylib", dst="lib", src="h5cpp", keep_path=False)
        else:
            self.copy("*.so", dst="lib", src="h5cpp", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)
        self.copy("LICENSE.*", src="h5cpp")

    def package_info(self):
        self.cpp_info.libs = ["h5cpp"]
