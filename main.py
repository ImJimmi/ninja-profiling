#!/usr/bin/env python
import argparse
import os
from os import getcwd

from log_symbols import LogSymbols

from profiling.cmake_ninja_build import cmake_ninja_build
from tracing.ninja_trace import generate_ninja_trace, parse_ninja_trace


def _profile_project(
    workspace: str,
    clean: bool,
    targets: list[str] = ["all"],
    cmake_generate_args: list[str] = [],
    filter_out_regexes: list[str] = [],
):
    for target in targets:
        print(f"Profile for `{workspace}` - `{target}`")

        cmake_build_dir = f"cmake-ninja-build-{target}"
        trace_filename = f"{target}.trace.json"

        if clean or not os.path.exists(f"{workspace}/{cmake_build_dir}/.ninja_log"):
            cmake_ninja_build(
                workspace=workspace,
                cmake_build_dir=cmake_build_dir,
                cmake_generate_args=cmake_generate_args,
            )
        else:
            print(f"{LogSymbols.WARNING.value} Skipped building")

        generate_ninja_trace(
            workspace=workspace,
            cmake_build_dir=cmake_build_dir,
            trace_filename=trace_filename,
        )
        parse_ninja_trace(
            workspace=workspace,
            trace_filename=trace_filename,
            filter_out_regexes=filter_out_regexes,
        )
        print()


def profile_hello_world(clean: bool):
    _profile_project(f"{getcwd()}/examples/hello-world", clean)


def profile_JUCE(clean: bool):
    _profile_project(
        f"{getcwd()}/examples/JUCE",
        clean,
        targets=["DemoRunner", "Projucer"],
        cmake_generate_args=[
            "-DJUCE_BUILD_EXTRAS=ON",
            "-DJUCE_BUILD_EXAMPLES=ON",
        ],
        filter_out_regexes=[r".*/modules/.*", r".*_binarydata_.*", r".*DemoPIPs.*"],
    )


def profile_Catch(clean: bool):
    _profile_project(
        f"{getcwd()}/examples/Catch2",
        clean,
        cmake_generate_args=["-DCATCH_BUILD_EXAMPLES=ON"],
    )


def profile_Surge(clean: bool):
    _profile_project(
        f"{getcwd()}/examples/Surge",
        clean,
        cmake_generate_args=["-DENABLE_LTO=OFF"],
        filter_out_regexes=[
            r".*/modules/.*",
            r".*libs/.*",
            r".*_binarydata_.*",
            r".*tests.*",
        ],
    )


def profile_JIVE(clean: bool):
    _profile_project(
        f"{getcwd()}/examples/JIVE",
        clean,
        cmake_generate_args=["-DJIVE_BUILD_DEMO_RUNNER=ON"],
        filter_out_regexes=[
            r".*/modules/.*",
            r".*_binarydata_.*",
        ],
    )


def profile_ADC23(clean: bool):
    _profile_project(
        f"{getcwd()}/examples/accessible-juce-app-adc-23",
        clean,
        filter_out_regexes=[
            r".*/modules/.*",
        ],
    )


def profile_fmt(clean: bool):
    _profile_project(
        f"{getcwd()}/examples/fmt",
        clean,
        cmake_generate_args=["-DFMT_TEST=ON", "-DFMT_FUZZ=ON"],
    )


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
        profile_hello_world(args.clean)
        profile_JUCE(args.clean)
        profile_Catch(args.clean)
        profile_Surge(args.clean)
        profile_JIVE(args.clean)
        profile_ADC23(args.clean)
        profile_fmt(args.clean)
    else:
        _profile_project(
            args.workspace,
            args.clean,
            cmake_generate_args=args.cmake_args,
            filter_out_regexes=args.filter_out_regexes,
        )
