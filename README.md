To reproduce run

```bash
bazel build //protos:sorting_service_python_proto
```

Error

```
Loading: loading...
INFO: Analyzed target //protos:sorting_service_python_proto (2 packages loaded, 348 targets configured).
INFO: Found 1 target...
ERROR: /home/rbhadauria/.cache/bazel/_bazel_rbhadauria/<readcted>/external/com_google_protobuf/BUILD:938:17: ProtoCompile external/com_google_protobuf/python/google/protobuf/compiler/plugin_pb2.py failed: (Aborted): protoc failed: error executing command bazel-out/k8-opt-exec-2B5CBBC6/bin/external/com_google_protobuf/protoc '--python_out=bazel-out/k8-fastbuild/bin/external/com_google_protobuf/python' -Iexternal/com_google_protobuf/python ... (remaining 2 argument(s) skipped)

Use --sandbox_debug to see verbose messages from the sandbox
external/com_google_protobuf/pythonuncaught_exceptions not yet implemented
Target //protos:sorting_service_python_proto failed to build
Use --verbose_failures to see the command lines of failed build steps.
INFO: Elapsed time: 0.607s, Critical Path: 0.02s
INFO: 12 processes: 12 internal.
FAILED: Build did NOT complete successfully
```
