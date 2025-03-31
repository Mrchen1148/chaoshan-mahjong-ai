FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

# Install required packages
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    build-essential \
    git \
    wget \
    unzip \
    openjdk-11-jdk \
    autoconf \
    libtool \
    pkg-config \
    zlib1g-dev \
    libncurses5-dev \
    libncursesw5-dev \
    libtinfo5 \
    cmake \
    && rm -rf /var/lib/apt/lists/*

# Install Android SDK
ENV ANDROID_HOME=/opt/android-sdk
ENV PATH=${PATH}:${ANDROID_HOME}/tools:${ANDROID_HOME}/platform-tools

RUN mkdir -p ${ANDROID_HOME} && \
    wget https://dl.google.com/android/repository/commandlinetools-linux-8512546_latest.zip && \
    unzip commandlinetools-linux-*_latest.zip -d ${ANDROID_HOME} && \
    rm commandlinetools-linux-*_latest.zip

# Accept licenses
RUN yes | ${ANDROID_HOME}/cmdline-tools/bin/sdkmanager --licenses

# Install required Android SDK packages
RUN ${ANDROID_HOME}/cmdline-tools/bin/sdkmanager \
    "platform-tools" \
    "platforms;android-31" \
    "build-tools;31.0.0" \
    "ndk;23.1.7779620"

# Install Python dependencies
COPY requirements.txt /app/
COPY requirements-app.txt /app/
WORKDIR /app

RUN pip3 install --upgrade pip && \
    pip3 install -r requirements.txt && \
    pip3 install -r requirements-app.txt && \
    pip3 install buildozer

# Copy application files
COPY . /app/

# Build APK
CMD buildozer android debug
