# Use a base image for Raspberry Pi 5 (64-bit, Bookworm)
# Using a generic arm64 debian image for broader compatibility
FROM debian:bookworm-slim

# Set environment variables to prevent interactive prompts during installation
ENV DEBIAN_FRONTEND=noninteractive
ENV LANG C.UTF-8

# Install system dependencies required for Kivy, OpenCV, and camera access
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Python and pip
    python3 \
    python3-pip \
    python3-setuptools \
    # Kivy dependencies
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libgstreamer1.0-dev \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-bad \
    gstreamer1.0-libav \
    # OpenCV dependencies
    libopencv-dev \
    python3-opencv \
    # General utilities
    git \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /usr/src/app

# Copy the application source code into the container
COPY ./app /usr/src/app

# Install Python dependencies from requirements.txt
# We use --break-system-packages as is standard in Debian 12 (Bookworm)
RUN pip3 install --no-cache-dir --break-system-packages -r requirements.txt

# Expose the display and input devices (though this is mainly handled in docker-compose)
# This command doesn't do much functionally but serves as documentation.
EXPOSE 0

# The command to run the application
# The user running the container must have access to video and input groups.
CMD ["python3", "main.py"]