# conan-aws-sdk-cpp

[![Build Status: Linux, OSX](https://travis-ci.org/SMelanko/conan-aws-sdk-cpp.svg?branch=master)](https://travis-ci.org/SMelanko/conan-aws-sdk-cpp)

Conan Package for [aws-sdk-cpp](https://github.com/aws/aws-sdk-cpp)

# How To Use

```py
from conans import ConanFile, CMake

class AppConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    
    requires = "aws-sdk-cpp/1.4.17@smela/testing"
    
    default_options = "aws-sdk-cpp:shared=False", \
        "aws-sdk-cpp:build_s3=True"
        
    generators = "cmake"
```
