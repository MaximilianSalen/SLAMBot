# Base image
FROM ubuntu:22.04

# Set environment variables to avoid interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Update the package list and install basic build tools
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    wget \
    unzip \
    libboost-dev \
    libboost-thread-dev \
    libboost-filesystem-dev \
    libgtk2.0-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*


# Install OpenCV dependencies
RUN apt-get update %% apt-get install -y \
    libopencv-dev \
    && rm -rf /var/lib/apt/lists/*


# Install Eigen3
RUN apt-get update && apt-get install -y \
    libeigen3-dev \
    && rm -rf /var/lib/apt/lists/*


# Install Pangolin (a visualization library required by ORB-SLAM2)
RUN apt-get update && apt-get install -y \
    libglew-dev \
    libpython2.7-dev \
    libglm-dev \
    && rm -rf /var/lib/apt/lists/*


# Clone and build Pangolin
RUN git clone https://github.com/stevenlovegrove/Pangolin.git /Pangolin && \
    cd /Pangolin && mkdir build && cd build && cmake .. && make -j && make install

# Clone and build ORB-SLAM2
RUN git clone https://github.com/raulmur/ORB_SLAM2.git /ORB_SLAM2 && \
    cd /ORB_SLAM2 && chmod +x build.sh && ./build.sh
