# conan-aws-sdk-cpp

[Conan.io](https://conan.io) package for the [aws-sdk-cpp](https://github.com/aws/aws-sdk-cpp)

## Reuse The Packages

### Add Remote

```bash
$ conan remote add <REMOTE> https://api.bintray.com/conan/toge-conan/conan 
```

You can fill any id in `<REMOTE>`.

### Basic setup

```bash
$ conan install aws-sdk-cpp/1.8.156@toge/stable
```

### Project setup

```py
from conans import ConanFile, CMake

class AppConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"

    requires = "aws-sdk-cpp/1.8.129@toge/stable"

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

### Build

Builds a binary package for recipe (conanfile.py) located in current dir. 
For more info please check [conan create](http://docs.conan.io/en/latest/reference/commands/creator/create.html#conan-create).

```bash
$ conan create . 1.8.156@toge/stable --build=missing
```

### Upload

Uploads a recipe and binary packages to a remote. 
For more info please check [conan upload](http://docs.conan.io/en/latest/reference/commands/creator/upload.html#conan-upload).

```bash
$ conan upload aws-sdk-cpp/1.8.156@toge/stable --all -r <REMOTE> 
```

Special thanks to @kmaragon for code base from scratch

Special thanks to @SMelanko for README and contributions beyond just gcc + linux
