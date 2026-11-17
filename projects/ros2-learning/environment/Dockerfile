FROM ros:jazzy

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ros-jazzy-navigation2 \
        ros-jazzy-nav2-bringup \
        ros-jazzy-nav2-minimal-tb3-sim \
        ros-jazzy-slam-toolbox \
        ros-jazzy-ros-gz \
        ros-jazzy-rviz2 \
        ros-jazzy-nav2-rviz-plugins \
        xvfb \
        x11vnc \
        novnc \
        websockify \
        openbox \
        dbus-x11 \
    && rm -rf /var/lib/apt/lists/*

COPY start-desktop.sh /usr/local/bin/start-amr-desktop
RUN chmod +x /usr/local/bin/start-amr-desktop

ENV DISPLAY=:1 \
    LIBGL_ALWAYS_SOFTWARE=1 \
    QT_X11_NO_MITSHM=1 \
    XDG_RUNTIME_DIR=/tmp/runtime-ros

WORKDIR /workspace
ENTRYPOINT ["/usr/local/bin/start-amr-desktop"]
