#!/usr/bin/env python
import argparse
import os
from os import getcwd

from log_symbols import LogSymbols

from benchmarking.cmake_ninja_build import cmake_ninja_build
from tracing.ninja_trace import generate_ninja_trace, parse_ninja_trace


def profile_hello_world():
    workspace = f"{getcwd()}/examples/hello-world"
    cmake_build_dir = "cmake-ninja-build"
    print(workspace)

    cmake_ninja_build(
        workspace=workspace,
        cmake_build_dir=cmake_build_dir,
    )
    generate_ninja_trace(workspace=workspace, cmake_build_dir=cmake_build_dir)
    parse_ninja_trace(workspace=workspace)
    print()


def profile_JUCE():
    workspace = f"{getcwd()}/examples/JUCE"

    for target in ["DemoRunner", "Projucer"]:
        print(f"{workspace} - {target}")
        trace_filename = f"{target}.trace.json"

        cmake_build_dir = f"cmake-ninja-build-{target}"

        if not os.path.exists(f"{workspace}/{cmake_build_dir}/.ninja_log"):
            cmake_ninja_build(
                workspace=workspace,
                cmake_build_dir=cmake_build_dir,
                cmake_generate_args=[
                    "-DJUCE_BUILD_EXTRAS=ON",
                    "-DJUCE_BUILD_EXAMPLES=ON",
                ],
                cmake_target=target,
            )

        generate_ninja_trace(
            workspace=workspace,
            cmake_build_dir=cmake_build_dir,
            trace_filename=trace_filename,
        )
        parse_ninja_trace(
            workspace=workspace,
            trace_filename=trace_filename,
            filter_out_regexes=[r".*/modules/.*", r".*_binarydata_.*", r".*DemoPIPs.*"],
        )
        print()


def profile_Catch():
    workspace = f"{getcwd()}/examples/Catch2"

    print(workspace)
    trace_filename = "trace.json"

    cmake_build_dir = f"cmake-ninja-build"

    if not os.path.exists(f"{workspace}/{cmake_build_dir}/.ninja_log"):
        cmake_ninja_build(
            workspace=workspace,
            cmake_build_dir=cmake_build_dir,
            cmake_generate_args=[
                "-DCATCH_BUILD_EXAMPLES=ON",
            ],
        )

    generate_ninja_trace(
        workspace=workspace,
        cmake_build_dir=cmake_build_dir,
        trace_filename=trace_filename,
    )
    parse_ninja_trace(
        workspace=workspace,
        trace_filename=trace_filename,
    )
    print()


def profile_Surge():
    workspace = f"{getcwd()}/examples/Surge"

    print(workspace)
    trace_filename = "trace.json"

    cmake_build_dir = f"cmake-ninja-build"

    if not os.path.exists(f"{workspace}/{cmake_build_dir}/.ninja_log"):
        cmake_ninja_build(
            workspace=workspace,
            cmake_build_dir=cmake_build_dir,
            cmake_generate_args=["-DENABLE_LTO=OFF"],
        )

    generate_ninja_trace(
        workspace=workspace,
        cmake_build_dir=cmake_build_dir,
        trace_filename=trace_filename,
    )
    parse_ninja_trace(
        workspace=workspace,
        trace_filename=trace_filename,
        filter_out_regexes=[
            r".*/modules/.*",
            r".*libs/.*",
            r".*_binarydata_.*",
            r".*tests.*",
        ],
    )
    print()


def profile_JIVE():
    workspace = f"{getcwd()}/examples/JIVE"

    print(workspace)
    trace_filename = "trace.json"

    cmake_build_dir = f"cmake-ninja-build"

    if not os.path.exists(f"{workspace}/{cmake_build_dir}/.ninja_log"):
        cmake_ninja_build(
            workspace=workspace,
            cmake_build_dir=cmake_build_dir,
            cmake_generate_args=["-DJIVE_BUILD_DEMO_RUNNER=ON"],
        )

    generate_ninja_trace(
        workspace=workspace,
        cmake_build_dir=cmake_build_dir,
        trace_filename=trace_filename,
    )
    parse_ninja_trace(
        workspace=workspace,
        trace_filename=trace_filename,
        filter_out_regexes=[
            r".*/modules/.*",
            r".*_binarydata_.*",
        ],
    )
    print()


def profile_ADC23():
    workspace = f"{getcwd()}/examples/accessible-juce-app-adc-23"

    print(workspace)
    trace_filename = "trace.json"

    cmake_build_dir = f"cmake-ninja-build"

    if not os.path.exists(f"{workspace}/{cmake_build_dir}/.ninja_log"):
        cmake_ninja_build(
            workspace=workspace,
            cmake_build_dir=cmake_build_dir,
        )

    generate_ninja_trace(
        workspace=workspace,
        cmake_build_dir=cmake_build_dir,
        trace_filename=trace_filename,
    )
    parse_ninja_trace(
        workspace=workspace,
        trace_filename=trace_filename,
        filter_out_regexes=[
            r".*/modules/.*",
        ],
    )
    print()


def profile_fmt():
    workspace = f"{getcwd()}/examples/fmt"

    print(workspace)
    trace_filename = "trace.json"

    cmake_build_dir = f"cmake-ninja-build"

    if not os.path.exists(f"{workspace}/{cmake_build_dir}/.ninja_log"):
        cmake_ninja_build(
            workspace=workspace,
            cmake_build_dir=cmake_build_dir,
            cmake_generate_args=["-DFMT_TEST=ON", "-DFMT_FUZZ=ON"],
        )

    generate_ninja_trace(
        workspace=workspace,
        cmake_build_dir=cmake_build_dir,
        trace_filename=trace_filename,
    )
    parse_ninja_trace(
        workspace=workspace,
        trace_filename=trace_filename,
    )
    print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Profile a Ninja build")
    parser.add_argument("--examples", action="store_true", help="Run the examples?")

    parser.add_argument(
        "--workspace",
        type=str,
        help="Which workspace to work from. Defaults to CWD",
        default=getcwd(),
    )
    parser.add_argument(
        "--targets",
        nargs="*",
        type=str,
        help="Which CMake targets to build",
        default=["all"],
    )
    parser.add_argument(
        "--cmake-args",
        nargs="*",
        type=str,
        help="Additional CMake args to pass to the generate step",
        default=[],
    )
    parser.add_argument(
        "--filter-out-regexes", nargs="*", type=str, help="Additional", default=[]
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Delete the CMake build folder and build from scratch?",
    )
    parser.add_argument(
        "--unity-size",
        type=int,
        help="The value to use for CMAKE_UNITY_BUILD_BATCH_SIZE. Values <0 will disable unity builds. Disabled by default.",
        default=-1,
    )

    args = parser.parse_args()

    if args.examples:
        profile_hello_world()
        profile_JUCE()
        profile_Catch()
        profile_Surge()
        profile_JIVE()
        profile_ADC23()
        profile_fmt()
    else:
        for target in args.targets:
            print(f"{args.workspace} - {target}")
            trace_filename = f"{target}.trace.json"

            cmake_build_dir = f"cmake-ninja-build-{target}"

            if args.clean or not os.path.exists(
                f"{args.workspace}/{cmake_build_dir}/.ninja_log"
            ):
                cmake_ninja_build(
                    workspace=args.workspace,
                    cmake_build_dir=cmake_build_dir,
                    cmake_generate_args=args.cmake_args,
                    cmake_target=target,
                    unity_size=args.unity_size,
                )
            else:
                print(f"{LogSymbols.WARNING.value} Skipped building")

            generate_ninja_trace(
                workspace=args.workspace,
                cmake_build_dir=cmake_build_dir,
                trace_filename=trace_filename,
            )
            parse_ninja_trace(
                workspace=args.workspace,
                trace_filename=trace_filename,
                filter_out_regexes=args.filter_out_regexes,
            )
            print()
