#!/bin/bash


# Exit on error
set -e


# Configuraion
BUILD_DIR="build"
CMAKE_GENERATOR="Ninja"
BUILD_TYPE="Release"
SYMLINK_NAME="run_slam"
EXECUTABLE_NAME="SLAMBot"
THIRD_PARTY_DIR="third_party"

# URLs for the third_party dependencies
SOPHUS_URL="https://github.com/strasdat/Sophus.git"
PANGOLIN_URL="https://github.com/stevenlovegrove/Pangolin.git"
G2O_URL="https://github.com/RainerKuemmerle/g2o.git"

# Function to download third-party dependencies
download_dependencies(){
    if [! -d "$THIRD_PARTY_DIR" ]; then
        echo "Creating third-party directory..."
        mkdir -p "$THIRD_PARTY_DIR"
    fi

    # Download 3PPs if they are not already downloaded
    if [ ! -d "$THIRD_PARTY_DIR/sophus" ]; then
        echo "Cloning Sophus..."
        git clone "$SOPHUS_URL" "$THIRD_PARTY_DIR/sophus"
    else
        echo "Sophus is already downloaded"
    fi

    if [ ! -d "$THIRD_PARTY_DIR/pangolin" ]; then
        echo "Cloning pangolin..."
        git clone --recursive "$PANGOLIN_URL" "$THIRD_PARTY_DIR/pangolin"
        ./third_party/pangolin/scripts/install_prerequisites.sh --dry-run recommended
    else
        echo "pangolin is already downloaded"
    fi

    if [ ! -d "$THIRD_PARTY_DIR/g2o" ]; then
        echo "Cloning g2o..."
        git clone "$G2O_URL" "$THIRD_PARTY_DIR/g2o"
    else
        echo "g2o is already downloaded"
    fi
}

# Function to cleanly build
clean_build() {
    echo "Cleaning build directory..."
    rm -rf "$BUILD_DIR"
    echo "Cleaned build directory."
}

# Function to build the project
build_project(){
    if [ ! -d "$BUILD_DIR" ]; then
        echo "Creating build directory: $BUILD_DIR"
        mkdir -p "$BUILD_DIR"
    fi


    cd "$BUILD_DIR"

    # Run CMake configuration
    echo "Configuring the project with CMake..."
    cmake -G "$CMAKE_GENERATOR" -DCMAKE_BUILD_TYPE="$BUILD_TYPE" ..

    # Build the project
    echo "Building the project with Ninja..."
    ninja

    cd ..

    # Create a symlink to run executable directly from root
    if [ ! -L "$SYMLINK_NAME"]; then
        target_file="$BUILD_DIR/$EXECUTABLE_NAME"
        if [ -f "$target_file" ]; then
            ln -s $targetfile $SYMLINK_NAME
            echo "Symlink created: $SYMLINK_NAME -> $target_file"
        else
            echo "Executable not found: $target_file. Skipping symlink creation."
        fi
    fi
}

# Function to run the executable
run_executable() {
    target_file="$BUILD_DIR/$EXECUTABLE_NAME"
    if [ -f "$target_file" ]; then
        echo "Running the executable..."
        "./$target_file"
    else
        echo "Executable not found: $target_file. Please build the project first."
        exit 1
    fi
}

# Parse command-line arguments
case "$1" in
    clean)
        clean_build
        download_dependencies
        build_project
        ;;
    run)
        build_project
        download_dependencies
        run_executable
        ;;
    build | "" )
        download_dependencies
        build_project
        ;;
    *)
        echo "Usage: $0 [clean|build|run]"
        exit 1
        ;;
esac
