# Base image
FROM ubuntu:22.04

# Set environment variables to avoid interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install basic dependencies and Python's pip to install CMake
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-pip \
    sudo \
    g++12 \
    pkg-config \
    libgl1-mesa-dev \
    libwayland-dev \
    libxkbcommon-dev \
    wayland-protocols \
    libc++-dev \
    libepoxy-dev \
    libglew-dev \
    libegl1-mesa-dev \
    libva-dev \
    libvdpau-dev \
    libx11-dev \
    libx11-xcb-dev \
    libfontenc-dev \
    libice-dev \
    libsm-dev \
    libxau-dev \
    libxaw7-dev \
    libxcomposite-dev \
    libxcursor-dev \
    libxdamage-dev \
    libxfixes-dev \
    libxi-dev \
    libxinerama-dev \
    libxkbfile-dev \
    libxmuu-dev \
    libxrandr-dev \
    libxrender-dev \
    libxres-dev \
    libxss-dev \
    libxtst-dev \
    libxv-dev \
    libxxf86vm-dev \
    libxcb-glx0-dev \
    libxcb-render0-dev \
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
    uuid-dev \
    libxcb-cursor-dev \
    libxcb-dri2-0-dev \
    libxcb-dri3-dev \
    libxcb-present-dev \
    libxcb-composite0-dev \
    libxcb-ewmh-dev \
    libxcb-res0-dev \
    libxcb-util-dev \
    libxcb-util0-dev \
    libjpeg-dev \
    libpng-dev \
    libeigen3-dev


RUN pip3 install uv

RUN useradd -m -s /bin/bash container-user

# Add the user to sudoers and allow passwordless sudo
RUN usermod -aG sudo container-user \
 && echo 'container-user ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/container-user \
 && chmod 0440 /etc/sudoers.d/container-user

# Switch to the new user
USER container-user
