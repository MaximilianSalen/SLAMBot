# Base image
FROM ubuntu:22.04

# Set environment variables to avoid interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install basic dependencies and Python's pip to install CMake
RUN apt-get update && apt-get install -y \
    build-essential \
    g++12 \
    python3-pip

RUN pip3 install uv
