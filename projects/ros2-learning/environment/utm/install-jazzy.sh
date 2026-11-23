#!/usr/bin/env bash
set -euo pipefail

# Run inside the installed Ubuntu 24.04 ARM64 guest, as its normal user.
source /etc/os-release
if [[ "${ID:-}" != ubuntu || "${VERSION_ID:-}" != 24.04 || "$(dpkg --print-architecture)" != arm64 ]]; then
  echo "Ubuntu 24.04 ARM64 is required." >&2
  exit 1
fi

sudo apt update
sudo apt install -y software-properties-common curl ca-certificates
sudo add-apt-repository -y universe

ros_apt_source_version="$(curl -fsSL https://api.github.com/repos/ros-infrastructure/ros-apt-source/releases/latest | python3 -c 'import json,sys; print(json.load(sys.stdin)["tag_name"])')"
ros_apt_source_deb="$(mktemp --suffix=.deb)"
trap 'rm -f "$ros_apt_source_deb"' EXIT
curl -fL --retry 3 -o "$ros_apt_source_deb" "https://github.com/ros-infrastructure/ros-apt-source/releases/download/${ros_apt_source_version}/ros2-apt-source_${ros_apt_source_version}.noble_all.deb"
sudo dpkg -i "$ros_apt_source_deb"

sudo apt update
sudo apt install -y \
  ros-jazzy-desktop \
  ros-jazzy-navigation2 \
  ros-jazzy-nav2-bringup \
  ros-jazzy-nav2-minimal-tb3-sim \
  ros-jazzy-slam-toolbox \
  ros-jazzy-ros-gz \
  ros-jazzy-nav2-rviz-plugins \
  qemu-guest-agent \
  spice-vdagent

if ! grep -Fqx 'source /opt/ros/jazzy/setup.bash' "$HOME/.bashrc"; then
  printf '\nsource /opt/ros/jazzy/setup.bash\n' >> "$HOME/.bashrc"
fi

# ROS setup files may reference unset environment variables.
set +u
source /opt/ros/jazzy/setup.bash
ros2 pkg prefix rviz2
ros2 pkg prefix nav2_bringup
ros2 pkg prefix slam_toolbox
printf '\nROS 2 packages are installed. Runtime simulation still needs verification.\n'
