# 🥷 Ninja Profiling

Analyse Ninja log files to profile build times.

```bash
$ ./main.py --workspace=./examples/Catch2 --targets=all --clean

Profile for `./examples/Catch2` - `all`
✔ Generated `./examples/Catch2/cmake-ninja-build-all` in 0.570s
✔ Built target `all` in 6.109s
✔ Generated `./examples/Catch2/all.trace.json` in 0.027s
✔ Parsed `./examples/Catch2/all.trace.json` in 0.008s
  ℹ Min:            0.051s  `src/CMakeFiles/Catch2.dir/Release/catch2/internal/catch_random_number_generator.cpp.o`
  ℹ Max:            2.072s  `src/CMakeFiles/Catch2.dir/Release/catch2/internal/catch_commandline.cpp.o`
  ℹ Median:         0.671s  `src/CMakeFiles/Catch2.dir/Release/catch2/internal/catch_wildcard_pattern.cpp.o`
  ℹ Mean:           0.701s
  ℹ Distribution:   |▂▁  ▁▅█▇▅▄▂▁ ▁▁        |
  ℹ TU Count:       105
```

```bash
$ ./main.py --help

usage: main.py [-h] [--examples] [--workspace WORKSPACE] [--targets [TARGETS ...]] [--cmake-args [CMAKE_ARGS ...]] [--filter-out-regexes [FILTER_OUT_REGEXES ...]] [--clean] [--unity-size UNITY_SIZE]

Profile a Ninja build

options:
  -h, --help            show this help message and exit
  --examples            Run the examples?
  --workspace WORKSPACE
                        Which workspace to work from. Defaults to CWD
  --targets [TARGETS ...]
                        Which CMake targets to build
  --cmake-args [CMAKE_ARGS ...]
                        Additional CMake args to pass to the generate step
  --filter-out-regexes [FILTER_OUT_REGEXES ...]
                        Additional
  --clean               Delete the CMake build folder and build from scratch?
  --unity-size UNITY_SIZE
                        The value to use for CMAKE_UNITY_BUILD_BATCH_SIZE. Values <0 will disable unity builds. Disabled by default.
```

## Prerequisites

The [ninjatracing](https://github.com/nico/ninjatracing) repo must be added to your PATH before running the script. Run `ninjatracing --help` to verify.

It's recommended to use a virtual environment, and install the dependencies from [`requirements.txt`](./requirements.txt):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Examples

The [`examples/`](./examples/) directory contains various submodules against which your own project can be compared. These need to be pulled before they can be profiled.

```bash
git submodule update --init --recursive
```

Running the script with the `--examples` flag will build and profile each of the examples, which may take some time.
