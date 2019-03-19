from conans import ConanFile, CMake, tools, RunEnvironment
import os


class GtestTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    requires = "cmake_installer/3.10.0@conan/stable"

    def build(self):
        cmake = CMake(self)
        # Current dir is "test_package/build/<build_id>" and CMakeLists.txt is
        # in "test_package".
        cmake.configure(source_dir=self.source_folder, build_dir="./")
        cmake.build()
        
    def imports(self):
        # Imports for Win32
        self.copy("*.dll", dst="bin", src="bin")
        self.copy("*.lib", dst="lib", src="bin")

    def test(self):
        os.chdir("bin")
        env_build = RunEnvironment(self)
        with tools.environment_append(env_build.vars):
          self.run(".%sexample" % os.sep)
