# Base image
FROM ubuntu:22.04

# Set environment variables to avoid interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install basic dependencies and Python's pip to install CMake
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    wget \
    cmake \
    g++ \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Install other dependencies (Eigen, OpenCV, etc.)
RUN apt-get update && apt-get install -y \
    libboost-dev \
    libepoxy-dev \
    libboost-thread-dev \
    libboost-filesystem-dev \
    libgl1-mesa-dev \
    libwayland-dev \
    libxkbcommon-dev \
    wayland-protocols \
    libegl1-mesa-dev \
    libc++-dev \
    libglew-dev \
    libeigen3-dev \
    ninja-build \
    libjpeg-dev \
    libpng-dev \
    catch2 \
    libavcodec-dev \
    libavutil-dev \
    libavformat-dev \
    libswscale-dev \
    libavdevice-dev \
    libgtk2.0-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Install OpenCV dependencies
RUN apt-get update && apt-get install -y \
    libopencv-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade cmake

# Install Sophus
RUN git clone https://github.com/strasdat/Sophus.git /Sophus && \
    cd /Sophus && \
    mkdir build && cd build && \
    cmake .. && make -j2 && make install

# Clone and build Pangolin
RUN git clone --recursive https://github.com/stevenlovegrove/Pangolin.git /Pangolin && \
    cd /Pangolin && mkdir build && cd build && \
    cmake .. && make -j$(nproc) && make install
