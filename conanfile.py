from conans import ConanFile, CMake, tools
import os

def merge_dicts_for_sdk(a, b):
    res = a.copy()
    res.update(b)
    return res

class AwssdkcppConan(ConanFile):
    name = "aws-sdk-cpp"
    version = "1.8.129"
    license = "Apache 2.0"
    url = "https://github.com/kmaragon/conan-aws-sdk-cpp"
    description = "Conan Package for aws-sdk-cpp"
    short_paths = True
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake_find_package_multi", "cmake"
    requires = "zlib/1.2.11"
    exports_sources = ["patch-cmakelists.patch", "patch-c-libs.patch"]
    sdks = ("access_management",
            "acm",
            "alexaforbusiness"
            "amplify"
            "apigateway",
            "application_autoscaling",
            "appstream",
            "appsync",
            "athena",
            "autoscaling",
            "batch",
            "budgets",
            "chime",
            "cloud9",
            "clouddirectory",
            "cloudformation",
            "cloudfront",
            "cloudhsmv2",
            "cloudsearch",
            "cloudtrail",
            "codebuild",
            "codecommit",
            "codedeploy",
            "codepipeline",
            "codestar",
            "cognito_identity",
            "cognito_idp",
            "cognito_sync",
            "comprehend",
            "config",
            "cur",
            "datapipeline",
            "dax",
            "devicefarm",
            "directconnect",
            "discovery",
            "dlm",
            "dms",
            "docdb",
            "ds",
            "dynamodb",
            "dynamodbstreams",
            "ec2",
            "ecr",
            "ecs",
            "eks",
            "elasticache",
            "elasticbeanstalk",
            "elasticfilesystem",
            "elasticloadbalancing",
            "elasticloadbalancingv2",
            "elasticmapreduce",
            "elastictranscoder",
            "email",
            "es",
            "events",
            "firehose",
            "fms",
            "fsx",
            "gamelift",
            "glacier",
            "globalaccelerator",
            "glue",
            "greengrass",
            "guardduty",
            "health",
            "iam",
            "identity_management",
            "importexport",
            "inspector",
            "iot_data",
            "iot_jobs_data",
            "iot",
            "kafka",
            "kinesis",
            "kinesisanalytics",
            "kinesisvideo",
            "kms",
            "lambda",
            "lex",
            "lightsail",
            "logs",
            "machinelearnings",
            "macie",
            "marketplace_entitlement",
            "marketplacecommerceanalytics",
            "mediaconvert",
            "medialive",
            "mediapackage",
            "mediastore",
            "mediatailor",
            "meteringmarketplace",
            "mobileanalytics",
            "monitoring",
            "mq",
            "mturk_requester",
            "neptune",
            "opsworks",
            "opsworkscm",
            "organizations",
            "pinpoint",
            "polly",
            "pricing",
            "queues",
            "quicksight",
            "ram",
            "rds",
            "redshift",
            "recognition",
            "resource_groups",
            "robomaker"
            "route53",
            "route53domains",
            "s3",
            "sagemaker",
            "sdb",
            "serverlessrepo"
            "servicecatalog",
            "servicediscovery",
            "shield",
            "signer",
            "sms",
            "snowball",
            "sns",
            "sqs",
            "ssm",
            "states",
            "storagegateway",
            "sts",
            "support",
            "swf",
            "text_to_speech",
            "texttract",
            "transcribe",
            "transfer",
            "translate",
            "waf",
            "workdocs",
            "worklink",
            "workmail",
            "workspaces",
            "xray"
           )
    options = merge_dicts_for_sdk({"build_" + x: [True, False] for x in sdks}, {
            "shared": [True, False],
            "min_size": [True, False]
        })
    default_options = ("shared=False","min_size=False") + tuple("build_" + x + "=False" for x in sdks)

    def requirements(self):
        if self.settings.os != "Windows":
            if self.settings.os != "Macos":
                self.requires("openssl/1.1.1d")
            self.requires("libcurl/7.66.0@bincrafters/stable")
        self.requires("aws-c-event-stream/[>= 0.1.5]")

    def source(self):
        tools.download("https://github.com/aws/aws-sdk-cpp/archive/%s.tar.gz" % self.version, "aws-sdk-cpp.tar.gz")
        tools.unzip("aws-sdk-cpp.tar.gz")
        os.unlink("aws-sdk-cpp.tar.gz")

        # patch the shipped CMakeLists.txt which builds stuff before even declaring a project
        # tools.patch(patch_file=os.path.join(self.source_folder, "patch-cmakelists.patch"))
        # tools.patch(patch_file=os.path.join(self.source_folder, "patch-c-libs.patch"))

        # This small hack might be useful to guarantee proper /MT /MD linkage in MSVC
        # if the packaged projewct doesn't have variables to set it properly
        tools.replace_in_file("aws-sdk-cpp-%s/CMakeLists.txt" % self.version, "project(\"aws-cpp-sdk-all\" VERSION \"${PROJECT_VERSION}\" LANGUAGES CXX)", '''project(aws-cpp-sdk-all VERSION "${PROJECT_VERSION}" LANGUAGES CXX)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()
''')
       
    def build(self):
        cmake = CMake(self)
        build_only = list([])
        for sdk in self.sdks:
            if getattr(self.options, "build_" + sdk):
                build_only.append(sdk)

        cmake.definitions["BUILD_DEPS"] = False
        cmake.definitions["BUILD_ONLY"] = ";".join(build_only)
        cmake.definitions["ENABLE_UNITY_BUILD"] = "ON"
        cmake.definitions["ENABLE_TESTING"] = "OFF"
        cmake.definitions["AUTORUN_UNIT_TESTS"] = "OFF"

        cmake.definitions["MINIMIZE_SIZE"] = "ON" if self.options.min_size else "OFF"
        cmake.definitions["BUILD_SHARED_LIBS"] = "ON" if self.options.shared else "OFF"
        cmake.definitions["FORCE_SHARED_CRT"] = "ON" if self.options.shared else "OFF"

        cmake.configure(source_folder="%s/aws-sdk-cpp-%s" % (self.source_folder, self.version), build_folder=self.build_folder)
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install(build_dir=self.build_folder)

        lib_path = os.path.join(self.package_folder, "lib")
        lib64_path = os.path.join(self.package_folder, "lib64")
        if os.path.exists(lib64_path):
            tools.rename(os.path.join(lib64_path, "aws-c-event-stream"), os.path.join(lib_path, "aws-c-event-stream"))
            tools.rename(os.path.join(lib64_path, "aws-c-common"), os.path.join(lib_path, "aws-c-common"))
            tools.rename(os.path.join(lib64_path, "aws-checksums"), os.path.join(lib_path, "aws-checksums"))
            tools.rename(os.path.join(lib64_path, "libaws-c-event-stream.a"), os.path.join(lib_path, "libaws-c-event-stream.a"))
            tools.rename(os.path.join(lib64_path, "libaws-c-common.a"), os.path.join(lib_path, "libaws-c-common.a"))
            tools.rename(os.path.join(lib64_path, "libaws-checksums.a"), os.path.join(lib_path, "libaws-checksums.a"))
            for entry in os.listdir(os.path.join(lib64_path, "cmake")):
                tools.rename(os.path.join(lib64_path, "cmake", entry), os.path.join(lib_path, "cmake", entry))
            os.rmdir(os.path.join(lib64_path, "cmake"))
            os.rmdir(lib64_path)

    def package_info(self):
        libs = list([])

        for sdk in self.sdks:
            if getattr(self.options, "build_" + sdk):
                libs.append("aws-cpp-sdk-" + sdk)
        libs.extend(["aws-cpp-sdk-core"])

        if self.settings.os == "Windows":
            libs.append("winhttp")
            libs.append("wininet")
            libs.append("bcrypt")
            libs.append("userenv")
            libs.append("version")
            libs.append("ws2_32")

        if self.settings.os == "Linux":
            libs.append("atomic")
            if self.settings.compiler == "clang":
                libs.append("-stdlib=libstdc++")

        self.cpp_info.libs = libs
        self.cpp_info.libdirs = ["lib"]
        self.cpp_info.includedirs = ["include"]
