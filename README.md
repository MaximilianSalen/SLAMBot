# SLAMBot

A Visual SLAM system implemented in C++ using OpenCV and Eigen.

## Build Project
The project is setup with [uv](https://github.com/astral-sh/uv) for managing
project tools. The project is built with [CMake](https://cmake.org/) and
[Ninja](https://ninja-build.org/) and the C++ packages are managed with [Conan](https://conan.io/). The developer environment is setup with [Docker](https://www.docker.com/).

The docker does not exist pre-built. To build it run
```sh
docker buildx build -t slambot-dev-env .
```
And to mount the project and enter with a bash shell
```sh
docker run --rm -it \
    -v $PWD:/workspace \
    -w /workspace \
    slambot-dev-env \
    bash
```

Once inside the container, run
```sh
uv sync
```
to install `uv` managed software. First time using `conan` the following command
will setup the `conan` profile.
```sh
uv run conan profile detect --force
```
Create a build directory in the root and enter it with
```sh
mkdir build
cd build
```
Install `conan` managed packages with
```sh
uv run conan install .. --output-folder=./conan --build=missing
```
Lastly, build the project with
```sh
uv run cmake .. -G Ninja -DCMAKE_BUILD_TYPE=Release
uv run ninja
```

From the build directory, the compiled program can be executed with
```sh
./SLAMBot/SLAMBot
```

## Utilities
Before a proper CI is setup the following tools are only provided as utilities.
### ClangFormat
[ClangFormat](https://clang.llvm.org/docs/ClangFormat.html) is used as a formatter for the C++ files.
