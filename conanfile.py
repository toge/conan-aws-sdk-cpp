from conans import ConanFile, CMake, tools
import os

def merge_dicts_for_sdk(a, b):
    res = a.copy()
    res.update(b)
    return res

class AwssdkcppConan(ConanFile):
    name = "aws-sdk-cpp"
    version = "1.4.17"
    license = "Apache 2.0"
    url = "https://github.com/SMelanko/conan-aws-sdk-cpp"
    description = "Conan Package for aws-sdk-cpp"
    short_paths = True
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    requires = "zlib/1.2.11@conan/stable"
    sdks = ("access_management",
            "acm",
            "alexaforbusiness"
            "apigateway",
            "application_autoscaling",
            "appstream",
            "appsync",
            "athena",
            "autoscaling",
            "batch",
            "budgets",
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
            "dms",
            "ds",
            "dynamodb",
            "dynamodbstreams",
            "ec2",
            "ecr",
            "ecs",
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
            "gamelift",
            "glacier",
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
            "kinesis",
            "kinesisanalytics",
            "kinesisvideo",
            "kms",
            "lambda",
            "lex",
            "lightsail",
            "logs",
            "machinelearnings",
            "marketplace_entitlement",
            "marketplacecommerceanalytics",
            "mediaconvert",
            "medialive",
            "mediapackage",
            "mediastore",
            "meteringmarketplace",
            "mobileanalytics",
            "monitoring",
            "mq",
            "mturk_requester",
            "opsworks",
            "opsworkscm",
            "organizations",
            "pinpoint",
            "polly",
            "pricing",
            "queues",
            "rds",
            "redshift",
            "recognition",
            "resource_groups",
            "route53",
            "route53domains",
            "s3",
            "sagemaker",
            "sdb",
            "serverlessrepo"
            "servicecatalog",
            "servicediscovery",
            "shield",
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
            "transfer",
            "translate",
            "waf",
            "workdocs",
            "workmail",
            "workspaces",
            "xray"
           )
    options = merge_dicts_for_sdk({"build_" + x: [True, False] for x in sdks}, {
            "shared": [True, False],
            "min_size": [True, False]
        })
    default_options = ("shared=False","min_size=False") + tuple("build_" + x + "=False" for x in sdks)

    def configure(self):
        if self.settings.os != "Windows":
            if self.settings.os != "Macos":
                self.requires("OpenSSL/1.0.2l@conan/stable")
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
        build_only = list([])
        for sdk in self.sdks:
            if getattr(self.options, "build_" + sdk):
                build_only.append(sdk)

        cmake.definitions["BUILD_ONLY"] = ";".join(build_only)
        cmake.definitions["ENABLE_UNITY_BUILD"] = "ON"
        cmake.definitions["ENABLE_TESTING"] = "OFF"
        cmake.definitions["AUTORUN_UNIT_TESTS"] = "OFF"

        cmake.definitions["MINIMIZE_SIZE"] = "ON" if self.options.min_size else "OFF"
        cmake.definitions["BUILD_SHARED_LIBS"] = "ON" if self.options.shared else "OFF"
         
        cmake.configure(source_dir="%s/aws-sdk-cpp-%s" % (self.source_folder, self.version))
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        libs = list([])
        for sdk in self.sdks:
            if getattr(self.options, "build_" + sdk):
                libs.append("aws-cpp-sdk-" + sdk)
        libs.append("aws-cpp-sdk-core")
        self.cpp_info.libs = libs
        self.cpp_info.libdirs = ["lib"]
        self.cpp_info.includedirs = ["include"]
