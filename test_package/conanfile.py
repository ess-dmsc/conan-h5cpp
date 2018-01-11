from conans import ConanFile, CMake, tools
import os


class GraylogloggerTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    def build(self):
        cmake = CMake(self)
        # Current dir is "test_package/build/<build_id>" and CMakeLists.txt is
        # in "test_package".
        cmake.configure(source_dir=self.conanfile_directory, build_dir="./")
        cmake.build()

    def imports(self):
        self.copy("*.dll", dst="bin", src="bin")
        self.copy("*.dylib*", dst="bin", src="lib")
        self.copy("*.so*", dst="bin", src="lib")

    def test(self):
        os.chdir("bin")

        if tools.os_info.is_linux:
            ld_library_path = os.environ.get("LD_LIBRARY_PATH", "")
            os.environ["LD_LIBRARY_PATH"] = ld_library_path + ":."

        self.run(".%sexample" % os.sep)
