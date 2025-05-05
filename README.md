SLAMBot
-------

A Visual SLAM system implemented in C++ using OpenCV and Eigen.

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
    --mount type=bind,source=$pwd,target=$pwd \
    slambot-dev-image
```
And enter the workspace in a bash shell
```sh
docker exec -w $pwd -it slambot-dev-container bash
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
Create directory `build` and install `conan` packages in `build/conan`.
```sh
uv run conan install . --output-folder=./build/conan --profile=conan/profiles/linux
```
Lastly, build the project with
```sh
uv run cmake -S . -B build/release -G Ninja -DCMAKE_BUILD_TYPE=Release
uv run cmake --build build/release
```

From the build directory, the compiled program can be executed with
```sh
./SLAMBot/SLAMBot
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
uv run ctest --test-dir build/release/SLAMBot
```

## Add C++ package
To add a new C++ package with `conan` simply add the package to the
[conanfile.txt](./conanfile.txt). Available packages and versions can be found
here [https://conan.io/center/recipes](https://conan.io/center/recipes). If the
package or version does not exist, it is possible to write your own recipe and
compile it yourself.

## Utilities
Before a proper CI is setup the following tools are only provided as utilities.
### ClangFormat
[ClangFormat](https://clang.llvm.org/docs/ClangFormat.html) is used as a
formatter for the C++ files. To format all `.h` and `.cpp` files run
```sh
find . -name "*.cpp" -o -name "*.h" | xargs uv run clang-format -i
```
