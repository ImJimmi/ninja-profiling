import os
from datetime import timedelta
from shutil import rmtree as delete_directory
from typing import Dict

from utils.CLI import Step, exec

CMakeTarget = str


def _generate(workspace, cmake_build_dir, cmake_args, unity_size):
    with Step(
        text=f"Generating Ninja build...",
        success_text=f"Generated `{workspace}/{cmake_build_dir}`",
    ):
        if os.path.exists(f"{workspace}/{cmake_build_dir}"):
            delete_directory(f"{workspace}/{cmake_build_dir}")

        command = [
            "cmake",
            "-B",
            cmake_build_dir,
            "-G",
            "Ninja Multi-Config",
        ] + cmake_args

        if unity_size >= 0:
            command = command + [
                "-DCMAKE_UNITY_BUILD=ON",
                f"-DCMAKE_UNITY_BUILD_BATCH_SIZE={unity_size}",
            ]
        else:
            command = command + [
                "-DCMAKE_UNITY_BUILD=OFF",
            ]

        exec(command, workspace)


def _build(workspace, cmake_build_dir, target):
    with Step(text=f"Building `{target}`...", success_text=f"Built target `{target}`"):
        exec(
            command=[
                "cmake",
                "--build",
                cmake_build_dir,
                "--config",
                "Release",
                "--target",
                target,
            ],
            workspace=workspace,
        )


def cmake_ninja_build(
    workspace: str,
    cmake_generate_args: list[str] = [],
    cmake_target: CMakeTarget = "all",
    cmake_build_dir="cmake-ninja-build",
    unity_size=-1,
):
    _generate(workspace, cmake_build_dir, cmake_generate_args, unity_size)
    _build(workspace, cmake_build_dir, cmake_target)
