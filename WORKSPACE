###################################
# Setup
###################################

workspace(name = "com_etsy_sorting_service_demo")

load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

python_version = "3.9"

rules_python_version = "0.10.0"

rules_python_sha256 = "56dc7569e5dd149e576941bdb67a57e19cd2a7a63cc352b62ac047732008d7e1"

rules_proto_grpc_version = "4.0.1"

rules_proto_grpc_sha256 = "28724736b7ff49a48cb4b2b8cfa373f89edfcb9e8e492a8d5ab60aa3459314c8"


###################################
# Python support
###################################

http_archive(
    name = "rules_python",
    sha256 = rules_python_sha256,
    strip_prefix = "rules_python-{}".format(rules_python_version),
    url = "https://github.com/bazelbuild/rules_python/archive/refs/tags/{}.tar.gz".format(rules_python_version),
)

load("@rules_python//python:repositories.bzl", "python_register_toolchains")

python_register_toolchains(
    name = "python3_9",
    # Available versions are listed in @rules_python//python:versions.bzl.
    python_version = python_version,
)

load("@python3_9//:defs.bzl", "interpreter")

# Rules proto
http_archive(
    name = "rules_proto_grpc",
    sha256 = rules_proto_grpc_sha256,
    strip_prefix = "rules_proto_grpc-{}".format(rules_proto_grpc_version),
    urls = ["https://github.com/rules-proto-grpc/rules_proto_grpc/archive/{}.tar.gz".format(rules_proto_grpc_version)],
)

load("@rules_proto_grpc//:repositories.bzl", "rules_proto_grpc_repos", "rules_proto_grpc_toolchains")

rules_proto_grpc_toolchains()

rules_proto_grpc_repos()

load("@rules_proto//proto:repositories.bzl", "rules_proto_dependencies", "rules_proto_toolchains")

rules_proto_dependencies()

rules_proto_toolchains()

# Rules proto python
load("@rules_proto_grpc//python:repositories.bzl", rules_proto_grpc_python_repos = "python_repos")

rules_proto_grpc_python_repos()

load("@com_github_grpc_grpc//bazel:grpc_deps.bzl", "grpc_deps")

grpc_deps()

load("@rules_python//python:pip.bzl", "pip_install")

pip_install(
    name = "pip_modules",
    timeout = 36000,
    python_interpreter_target = interpreter,
    requirements = "requirements.txt",
)
