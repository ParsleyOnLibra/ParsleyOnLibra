#!/usr/bin/env bash
set -eo pipefail

source /opt/ros/jazzy/setup.bash
exec ros2 launch nav2_bringup tb3_simulation_launch.py \
  slam:=True \
  headless:=True \
  rviz_config_file:=/workspace/environment/nav2-browser.rviz
