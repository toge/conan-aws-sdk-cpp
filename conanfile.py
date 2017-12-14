from conans import ConanFile, CMake, tools
import os

class AwssdkcppConan(ConanFile):
    name = "aws-sdk-cpp"
    version = "1.3.22"
    license = "Apache 2.0"
    url = "https://github.com/kmaragon/conan-aws-sdk-cpp"
    description = "Conan Package for aws-sdk-cpp"
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
        "min_size": [True, False],
    }
    default_options = "shared=False","min_size=False"
    generators = "cmake"
    requires = "zlib/1.2.11@conan/stable"

    def configure(self):
        if self.settings.os != "Windows":
            if self.settings.os != "Macos":
                self.requires("OpenSSL/1.0.2m@conan/stable")
            self.requires("libcurl/7.56.1@bincrafters/stable")
           

    def source(self):
        tools.download("https://github.com/aws/aws-sdk-cpp/archive/%s.tar.gz" % self.version, "aws-sdk-cpp.tar.gz")
        tools.unzip("aws-sdk-cpp.tar.gz")
        os.unlink("aws-sdk-cpp.tar.gz")

        # This small hack might be useful to guarantee proper /MT /MD linkage in MSVC
        # if the packaged project doesn't have variables to set it properly
        tools.replace_in_file("aws-sdk-cpp-%s/CMakeLists.txt" % self.version, "project(\"aws-cpp-sdk-all\" VERSION \"${PROJECT_VERSION}\" LANGUAGES CXX)", '''project(aws-cpp-sdk-all VERSION "${PROJECT_VERSION}" LANGUAGES CXX)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

    def build(self):
        cmake = CMake(self)
        cmake.definitions["ENABLE_UNITY_BUILD"] = "ON"
        cmake.definitions["ENABLE_TESTING"] = "OFF"
        cmake.definitions["AUTORUN_UNIT_TESTS"] = "OFF"
        # TODO: some special if's will be needed for this
        # cmake.definitions["CPP_STANDARD"] = "14"

        cmake.definitions["MINIMIZE_SIZE"] = "ON" if self.options.min_size else "OFF"
        cmake.definitions["BUILD_SHARED_LIBS"] = "ON" if self.options.shared else "OFF"
         
        cmake.configure(source_dir="%s/aws-sdk-cpp-%s" % (self.source_folder, self.version))
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self, folder="lib")
        self.cpp_info.libdirs = ["lib"]
        self.cpp_info.includedirs = ["include"]
