from conans import ConanFile, CMake, tools
import os

def merge_dicts_for_sdk(a, b):
    res = a.copy()
    res.update(b)
    return res

class AwssdkcppConan(ConanFile):
    name = "aws-sdk-cpp"
    version = "1.8.145"
    license = "Apache 2.0"
    url = "https://github.com/toge/conan-aws-sdk-cpp"
    description = "Conan Package for aws-sdk-cpp"
    short_paths = True
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake_find_package_multi", "cmake"
    requires = "zlib/1.2.11"
    sdks = ("accessanalyzer",
        "acm",
        "acm-pca",
        "alexaforbusiness",
        "amp",
        "amplify",
        "amplifybackend",
        "apigateway",
        "apigatewaymanagementapi",
        "apigatewayv2",
        "appconfig",
        "appflow",
        "appintegrations",
        "application-autoscaling",
        "application-insights",
        "appmesh",
        "appstream",
        "appsync",
        "athena",
        "auditmanager",
        "autoscaling",
        "autoscaling-plans",
        "transfer",
        "backup",
        "batch",
        "braket",
        "budgets",
        "ce",
        "chime",
        "cloud9",
        "clouddirectory",
        "cloudformation",
        "cloudfront",
        "cloudhsm",
        "cloudhsmv2",
        "cloudsearch",
        "cloudsearchdomain",
        "cloudtrail",
        "codeartifact",
        "codebuild",
        "codecommit",
        "codedeploy",
        "codeguru-reviewer",
        "codeguruprofiler",
        "codepipeline",
        "codestar",
        "codestar-connections",
        "codestar-notifications",
        "cognito-identity",
        "cognito-idp",
        "cognito-sync",
        "comprehend",
        "comprehendmedical",
        "compute-optimizer",
        "config",
        "connect",
        "connect-contact-lens",
        "connectparticipant",
        "cur",
        "customer-profiles",
        "databrew",
        "dataexchange",
        "datapipeline",
        "datasync",
        "dax",
        "detective",
        "devicefarm",
        "devops-guru",
        "directconnect",
        "discovery",
        "dlm",
        "dms",
        "docdb",
        "ds",
        "dynamodb",
        "dynamodbstreams",
        "ebs",
        "ec2",
        "ec2-instance-connect",
        "ecr",
        "ecr-public",
        "ecs",
        "eks",
        "elastic-inference",
        "elasticache",
        "elasticbeanstalk",
        "elasticfilesystem",
        "elasticloadbalancing",
        "elasticloadbalancingv2",
        "elasticmapreduce",
        "elastictranscoder",
        "email",
        "emr-containers",
        "es",
        "eventbridge",
        "events",
        "firehose",
        "fms",
        "forecast",
        "forecastquery",
        "frauddetector",
        "fsx",
        "gamelift",
        "glacier",
        "globalaccelerator",
        "glue",
        "greengrass",
        "greengrassv2",
        "groundstation",
        "guardduty",
        "health",
        "healthlake",
        "honeycode",
        "iam",
        "identitystore",
        "imagebuilder",
        "importexport",
        "inspector",
        "iot",
        "iot-data",
        "iot-jobs-data",
        "iot1click-devices",
        "iot1click-projects",
        "iotanalytics",
        "iotdeviceadvisor",
        "iotevents",
        "iotevents-data",
        "iotfleethub",
        "iotsecuretunneling",
        "iotsitewise",
        "iotthingsgraph",
        "iotwireless",
        "ivs",
        "kafka",
        "kendra",
        "kinesis",
        "kinesis-video-archived-media",
        "kinesis-video-media",
        "kinesis-video-signaling",
        "kinesisanalytics",
        "kinesisanalyticsv2",
        "kinesisvideo",
        "kms",
        "lakeformation",
        "lambda",
        "lex",
        "lex-models",
        "lexv2-models",
        "lexv2-runtime",
        "license-manager",
        "lightsail",
        "location",
        "logs",
        "lookoutvision",
        "machinelearning",
        "macie",
        "macie2",
        "managedblockchain",
        "marketplace-catalog",
        "marketplace-entitlement",
        "marketplacecommerceanalytics",
        "mediaconnect",
        "mediaconvert",
        "medialive",
        "mediapackage",
        "mediapackage-vod",
        "mediastore",
        "mediastore-data",
        "mediatailor",
        "meteringmarketplace",
        "migrationhub-config",
        "mobile",
        "mobileanalytics",
        "monitoring",
        "mq",
        "mturk-requester",
        "mwaa",
        "neptune",
        "network-firewall",
        "networkmanager",
        "opsworks",
        "opsworkscm",
        "organizations",
        "outposts",
        "personalize",
        "personalize-events",
        "personalize-runtime",
        "pi",
        "pinpoint",
        "pinpoint-email",
        "polly",
        "pricing",
        "qldb",
        "qldb-session",
        "quicksight",
        "ram",
        "rds",
        "rds-data",
        "redshift",
        "redshift-data",
        "rekognition",
        "resource-groups",
        "resourcegroupstaggingapi",
        "robomaker",
        "route53",
        "route53domains",
        "route53resolver",
        "s3",
        "s3control",
        "s3outposts",
        "sagemaker",
        "sagemaker-a2i-runtime",
        "sagemaker-edge",
        "sagemaker-featurestore-runtime",
        "sagemaker-runtime",
        "savingsplans",
        "schemas",
        "sdb",
        "secretsmanager",
        "securityhub",
        "serverlessrepo",
        "service-quotas",
        "servicecatalog",
        "servicecatalog-appregistry",
        "servicediscovery",
        "sesv2",
        "shield",
        "signer",
        "sms",
        "sms-voice",
        "snowball",
        "sns",
        "sqs",
        "ssm",
        "sso",
        "sso-admin",
        "sso-oidc",
        "states",
        "storagegateway",
        "sts",
        "support",
        "swf",
        "synthetics",
        "textract",
        "timestream-query",
        "timestream-write",
        "transcribe",
        "transcribestreaming",
        "translate",
        "waf",
        "waf-regional",
        "wafv2",
        "wellarchitected",
        "workdocs",
        "worklink",
        "workmail",
        "workmailmessageflow",
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
            self.requires("libcurl/[>= 7.66.0]")
        self.requires("aws-c-event-stream/[>= 0.1.5]")

    def source(self):
        tools.download("https://github.com/aws/aws-sdk-cpp/archive/%s.tar.gz" % self.version, "aws-sdk-cpp.tar.gz")
        tools.unzip("aws-sdk-cpp.tar.gz")
        os.unlink("aws-sdk-cpp.tar.gz")

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
            if self.settings.compiler == "clang":
                libs.append("-stdlib=libstdc++")

        self.cpp_info.libs = libs
        self.cpp_info.libdirs = ["lib"]
        self.cpp_info.includedirs = ["include"]
