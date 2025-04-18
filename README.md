# SLAMBot

A Visual SLAM system implemented in C++ using OpenCV and Eigen.

## Build Project
The project is setup with [uv](https://github.com/astral-sh/uv) for managing
project tools. The project is built with [CMake](https://cmake.org/) and
[Ninja](https://ninja-build.org/) and the C++ packages are managed with [Conan](https://conan.io/).

Run
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
uv run cmake .. -G Ninja
ninja
```
