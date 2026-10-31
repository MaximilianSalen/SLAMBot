SLAMBot
-------

A Visual SLAM system implemented in C++ using OpenCV and Eigen.

The plan, decisions and conventions are in [docs/ROADMAP.md](./docs/ROADMAP.md).

## Clone Project
```
git clone git@github.com:MaximilianSalen/SLAMBot.git
```

## Layout
- [slambot](./slambot): the library, one CMake target per module
  (`slambot::core`, ...). Unit tests sit next to the code as `<file>_test.cpp`.
- [experiments](./experiments): book exercises and package demos.
- [cmake](./cmake): `slambot_add_module()`, warnings and sanitizers.

## Build Project
The project is setup with [uv](https://github.com/astral-sh/uv) for managing
project tools. The project is built with [CMake](https://cmake.org/) and
[Ninja](https://ninja-build.org/) and the C++ packages are managed with
[Conan](https://conan.io/). The developer environment is setup with
[Docker](https://www.docker.com/).

The docker does not exist pre-built. To build it run
```sh
docker buildx build -t slambot-dev-image .
```
Start the container with
```sh
docker run -td --name slambot-dev-container \
    --mount type=bind,source=$PWD,target=$PWD \
    slambot-dev-image
```
And enter the workspace in a bash shell
```sh
docker exec -w $PWD -it slambot-dev-container bash
```
Alternatively, open the project in VS Code and run "Dev Containers: Reopen in
Container". [.devcontainer/devcontainer.json](./.devcontainer/devcontainer.json)
builds the same image and mounts the workspace at the same path.

Once inside the container, run
```sh
uv sync
```
to install `uv` managed software. First time using `conan` the following command
will setup the `conan` profile.
```sh
uv run conan profile detect --force
```
Install the `conan` packages with the versions pinned in
[conan.lock](./conan.lock). Packages without a prebuilt binary for the profile
are built from source (`--build=missing`), so the first run takes a while.
```sh
uv run conan install . --profile=conan/profiles/linux --lockfile=conan.lock --build=missing
```
This generates the CMake toolchain and presets in `build/Release/generators`,
and a `CMakeUserPresets.json` (not committed) that includes them. Lastly,
configure and build the project with
```sh
uv run cmake --preset conan-release
uv run cmake --build --preset conan-release
```

When exiting the docker container, it can be stopped with
```sh
docker container stop slambot-dev-container
```

## Testing
The project uses [Catch2](https://github.com/catchorg/Catch2) for tests. A
module lists its test files under `TESTS` in `slambot_add_module()` (see
[slambot/core/CMakeLists.txt](./slambot/core/CMakeLists.txt)). Run the tests
with
```sh
uv run ctest --preset conan-release
```

To find memory errors and undefined behavior, build and test with
AddressSanitizer in `build/asan` (use `tsan` for ThreadSanitizer). It reuses
the packages from `conan install` above.
```sh
uv run cmake --preset asan
uv run cmake --build --preset asan
uv run ctest --preset asan
```

## Datasets
[scripts/datasets.py](./scripts/datasets.py) downloads EuRoC sequences into
`data/` (or `$SLAMBOT_DATA`). List them, then download the ones you need
```sh
uv run scripts/datasets.py list
uv run scripts/datasets.py download MH_01_easy V1_01_easy
```
EuRoC may only be used non-commercially, so `data/` is never committed. Note
that `git clean -x` deletes it.

Plot a ground-truth trajectory with [evo](https://github.com/MichaelGrupp/evo).
`--plot` opens a window, which needs Tk (on Arch: `sudo pacman -S tk`). In the
container, use `--save_plot <file>.png` instead.
```sh
uv run evo_traj euroc data/euroc/MH_01_easy/mav0/state_groundtruth_estimate0/data.csv --plot
```

## Experiments
Book exercises and package demos live in [experiments](./experiments). They are
built by default, but are not part of the library and are not run as tests.
`demo_opencv` opens a window, so it needs a display. To skip the experiments,
configure with
```sh
uv run cmake --preset conan-release -DSLAMBOT_BUILD_EXPERIMENTS=OFF
```

## Add C++ package
To add a new C++ package with `conan` simply add the package to the
[conanfile.txt](./conanfile.txt). Available packages and versions can be found
here [https://conan.io/center/recipes](https://conan.io/center/recipes). If the
package or version does not exist, it is possible to write your own recipe and
compile it yourself. Then update [conan.lock](./conan.lock) with
```sh
uv run conan lock create . --profile=conan/profiles/linux
```

## Utilities
### ClangFormat
[ClangFormat](https://clang.llvm.org/docs/ClangFormat.html) is used as a
formatter for the C++ files, and the [CI](./.github/workflows/ci.yml) checks
it. To format all C++ files in the repository run
```sh
git ls-files -- '*.cpp' '*.hpp' '*.h' | xargs uv run clang-format -i
```

### ClangTidy
[ClangTidy](https://clang.llvm.org/extra/clang-tidy/) checks the naming style
([ROADMAP D5](./docs/ROADMAP.md#d5-naming)) and common bugs in
`slambot/`, and the CI checks it. After a build, run
```sh
git ls-files -- 'slambot/*.cpp' | xargs uv run clang-tidy -p build/Release
```
