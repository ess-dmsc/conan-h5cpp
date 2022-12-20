from conans import ConanFile, CMake, tools, RunEnvironment
import os


class H5cppTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake", "cmake_find_package"
    options = {
        "with_boost": [True, False]
    }
    default_options = (
        "with_boost=False"
    )

    def build(self):
        cmake = CMake(self)
        
        if self.options.with_boost:
            cmake.definitions["WITH_BOOST"] = "ON"
        else:
            cmake.definitions["WITH_BOOST"] = "OFF"
                
        # Current dir is "test_package/build/<build_id>" and CMakeLists.txt is
        # in "test_package".
        cmake.configure(source_dir=self.source_folder, build_dir="./")
        cmake.build()
        
    def imports(self):
        # Imports for Win32
        self.copy("*.dll", dst="bin", src="bin")
        self.copy("*.lib", dst="lib", src="bin")
        self.copy("*.dylib*", dst="bin", src="lib")
        self.copy("*.so*", dst="bin", src="lib")

    def test(self):
        os.chdir("bin")
        env_build = RunEnvironment(self)
        with tools.environment_append(env_build.vars):
          self.run(".%sexample" % os.sep)
