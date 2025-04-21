# Base image
FROM ubuntu:22.04

# Set environment variables to avoid interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install basic dependencies and Python's pip to install CMake
RUN apt-get update && apt-get install -y \
    build-essential \
    g++12 \
    python3-pip \
    libegl-dev \
    libegl11-mesa-dev \
    libgtk2.0-dev \
    libva-dev \
    libvdpau-dev \
    libx11-dev \
    libx11-xcb-dev \
    libfontenc-dev \
    libice-dev \
    libsm-dev \
    libxau-dev \
    libxaw7-dev \
    libxkbfile-dev \
    libxmuu-dev \
    libxres-dev \
    libxss-dev \
    libxtst-dev \
    libxv-dev \
    libxxf86vm-dev \
    libxcb-glx0-dev \
    libxcb-render-util0-dev \
    libxcb-xkb-dev \
    libxcb-icccm4-dev \
    libxcb-image0-dev \
    libxcb-keysyms1-dev \
    libxcb-randr0-dev \
    libxcb-shape0-dev \
    libxcb-sync-dev \
    libxcb-xfixes0-dev \
    libxcb-xinerama0-dev \
    libxcb-dri3-dev \
    libxcb-cursor-dev \
    libxcb-dri2-0-dev \
    libxcb-dri3-dev \
    libxcb-present-dev \
    libxcb-composite0-dev \
    libxcb-ewmh-dev \
    libxcb-res0-dev \
    libxcb-util-dev \
    libxcb-util0-dev

RUN pip3 install uv
