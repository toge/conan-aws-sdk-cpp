# conan-aws-sdk-cpp
=====================================

[Conan.io](https://conan.io) package for the [aws-sdk-cpp](https://github.com/aws/aws-sdk-cpp)

## Package Status

| Bintray | Windows | Linux & macOS |
|:--------:|:---------:|:-----------------:|
|[![Download](https://api.bintray.com/packages/smela/conan/aws-sdk-cpp%3Asmela/images/download.svg) ](https://bintray.com/smela/conan/aws-sdk-cpp%3Asmela/_latestVersion)|[![Build status: Windows](https://ci.appveyor.com/api/projects/status/h2vsu09qrs0v4wew?svg=true)](https://ci.appveyor.com/project/SMelanko/conan-aws-sdk-cpp)|[![Build Status: Linux, OSX](https://travis-ci.org/SMelanko/conan-aws-sdk-cpp.svg?branch=master)](https://travis-ci.org/SMelanko/conan-aws-sdk-cpp)

## Reuse The Packages

### Basic setup

    $ conan install aws-sdk-cpp/1.4.17@smela/testing

### Project setup

```py
from conans import ConanFile, CMake

class AppConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    
    requires = "aws-sdk-cpp/1.4.17@smela/testing"
    
    default_options = "aws-sdk-cpp:shared=False", \
        "aws-sdk-cpp:build_s3=True"
        
    generators = "cmake"
```

Complete the installation of requirements for your project running:

    conan install .

Project setup installs the libraries (and all needed dependencies) and generates
the files *conanbuildinfo.txt* and *conanbuildinfo.cmake*
with all the paths and variables that you need to link with your dependencies.

Follow the Conan getting started: http://docs.conan.io
