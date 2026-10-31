SLAMBot
-------

A Visual SLAM system implemented in C++ using OpenCV and Eigen.

## Clone Project
```
git clone --recurse-submodules git@github.com:MaximilianSalen/SLAMBot.git
```
If the project is already cloned without the submodules, fetch them with
```
git submodule update --init --recursive
```

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

The compiled program can be executed with
```sh
./build/Release/SLAMBot/SLAMBotApp
```

When exiting the docker container, it can be stopped with
```sh
docker container stop slambot-dev-container
```

## Testing
The project use [Catch2](https://github.com/catchorg/Catch2) for tests. Tests
are added in their libraries respective CMake file. The tests can be run with
the following command
```sh
uv run ctest --preset conan-release
```

## Experiments
Book exercises and package demos live in [experiments](./experiments). They are
built by default, but are not part of the library and are not run as tests.
`demo_opencv` and `demo_pangolin` open a window, so they need a display. To skip
the experiments, configure with
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
it. To format all `.h` and `.cpp` files in the repository (not `extern`) run
```sh
git ls-files -- '*.cpp' '*.h' ':!extern/' | xargs uv run clang-format -i
```
