# 로컬 ROS 2 AMR 시뮬레이션 환경

Apple Silicon macOS의 Docker Desktop에서 ARM64 Ubuntu 24.04 기반 ROS 2 Jazzy, Gazebo Harmonic, Nav2, SLAM Toolbox 및 RViz를 실행하기 위한 환경입니다. 브라우저 화면은 로컬 `http://localhost:6080/vnc.html`에서 열립니다.

## 시작

Docker Desktop이 실행 중인 상태에서 이 폴더에서 다음을 실행합니다. 최초 빌드는 수 GB의 패키지를 내려받습니다.

```bash
docker compose up -d --build
docker compose exec amr_ros bash /workspace/environment/run-slam.sh
```

첫 명령은 컨테이너와 가상 데스크톱을 시작합니다. 두 번째 명령은 Gazebo·Nav2·SLAM Toolbox·RViz를 실행하며 실행 중 터미널을 점유합니다. `headless:=True`는 Gazebo의 3D 창을 생략합니다. RViz는 브라우저에서 `http://localhost:6080/vnc.html`을 열고 **Connect**를 눌러 봅니다. Docker 포트는 Mac의 `127.0.0.1`에만 연결됩니다.

RViz에서 목표를 지정해 주행하거나, 새 Mac 터미널에서 아래처럼 가상 로봇에 목표를 보낼 수 있습니다. 예제 세계의 시작점 `(0, 0)`에서 `(0.5, 0)`까지 이동하는 검증용 명령입니다.

```bash
docker compose exec amr_ros bash -lc 'source /opt/ros/jazzy/setup.bash; ros2 action send_goal /navigate_to_pose nav2_msgs/action/NavigateToPose "{pose: {header: {frame_id: map}, pose: {position: {x: 0.5, y: 0.0, z: 0.0}, orientation: {w: 1.0}}}}"'
```

지도 저장은 다른 Mac 터미널에서 실행합니다. 이 실습에서는 기본 저장 대기시간이 한 번 부족해 10초로 늘렸습니다.

```bash
docker compose exec amr_ros bash -lc 'source /opt/ros/jazzy/setup.bash; ros2 run nav2_map_server map_saver_cli -f /workspace/evidence/amr_map --ros-args -p save_map_timeout:=10.0'
```

저장 지도로 주행하려면 앞선 실행을 `Ctrl-C`로 끝내거나 `docker compose restart amr_ros`로 재시작한 뒤 다음을 실행합니다.

```bash
docker compose exec amr_ros bash /workspace/environment/run-navigation.sh
```

RViz에서 **2D Pose Estimate**로 시작 위치를 지정하거나 `/initialpose`를 발행한 뒤 목표를 보냅니다. 예제 세계의 시작 위치는 `(0, 0)`입니다. 전체 컨테이너 중지 명령은 `docker compose down`입니다.

## 현재 검증 상태

2026-11-18에 이 Mac에서 ROS 2 Jazzy, Gazebo 8.15.0, Nav2, SLAM Toolbox, RViz를 실행했습니다. SLAM 지도 저장과 저장 지도 기반 목표 주행까지 확인했습니다. 명령·결과·한계는 [`../evidence/2026-11-18-environment.md`](../evidence/2026-11-18-environment.md)에 기록했습니다.
