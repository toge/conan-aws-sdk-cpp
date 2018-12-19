# conan-aws-sdk-cpp

[Conan.io](https://conan.io) package for the [aws-sdk-cpp](https://github.com/aws/aws-sdk-cpp)

## Package Status

| Bintray | Windows | Linux & macOS |
|:--------:|:---------:|:-----------------:|
|[![Download](https://api.bintray.com/packages/kmaragon/conan/aws-sdk-cpp%3Akmaragon/images/download.svg) ](https://bintray.com/kmaragon/conan/aws-sdk-cpp%3Akmaragon/_latestVersion)|[![Build status: Windows](https://ci.appveyor.com/api/projects/status/bigap8u02pa3hsfa?svg=true)](https://ci.appveyor.com/project/kmaragon/conan-aws-sdk-cpp)|[![Build Status: Linux, OSX](https://travis-ci.org/kmaragon/conan-aws-sdk-cpp.svg?branch=master)](https://travis-ci.org/kmaragon/conan-aws-sdk-cpp)

## Reuse The Packages

### Basic setup

```bash
$ conan install aws-sdk-cpp/1.7.7@kmaragon/stable
```

### Project setup

```py
from conans import ConanFile, CMake

class AppConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"

    requires = "aws-sdk-cpp/1.7.7@kmaragon/stable"

    default_options = "aws-sdk-cpp:shared=False", \
        "aws-sdk-cpp:build_s3=True"

    generators = "cmake"
```

Complete the installation of requirements for your project running:

```bash
conan install .
```

Project setup installs the libraries (with all needed dependencies) and generates
the files *conanbuildinfo.txt* and *conanbuildinfo.cmake*
with all the paths and variables that you need to link with your dependencies.

Follow the Conan getting started: http://docs.conan.io.

## Publish The Package

The example below shows the commands used to publish to conan repository.

### Add Remote

```bash
$ conan remote add kmaragon https://api.bintray.com/conan/kmaragon/conan
```

### Build

Builds a binary package for recipe (conanfile.py) located in current dir. 
For more info please check [conan create](http://docs.conan.io/en/latest/reference/commands/creator/create.html#conan-create).

```bash
$ conan create . kmaragon/stable
```

### Upload

Uploads a recipe and binary packages to a remote. 
For more info please check [conan upload](http://docs.conan.io/en/latest/reference/commands/creator/upload.html#conan-upload).

```bash
$ conan upload aws-sdk-cpp/1.7.7@kmaragon/stable --all -r kmaragon 
```

Special thanks to @SMelanko for README and contributions beyond just gcc + linux
