#!/usr/bin/env bash
set -eo pipefail

map_file="${1:-/workspace/evidence/amr_map.yaml}"
if [[ ! -f "$map_file" ]]; then
  echo "Map not found: $map_file" >&2
  exit 1
fi

source /opt/ros/jazzy/setup.bash
exec ros2 launch nav2_bringup tb3_simulation_launch.py \
  slam:=False \
  map:="$map_file" \
  headless:=True \
  rviz_config_file:=/workspace/environment/nav2-browser.rviz
