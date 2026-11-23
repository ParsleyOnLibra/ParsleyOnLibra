# UTM Ubuntu의 ROS 2 Jazzy 설치 기록 — 2026-11-24

## 환경

- 2026-11-23에 부팅·로그인을 확인한 UTM Ubuntu 24.04.4 ARM64 데스크톱 VM에서 계속 진행했습니다.
- VM 구성과 초기 부팅 문제는 [전날 설치 기록](2026-11-23-utm-install.md)에 있습니다.

## 실제 실행·관찰

1. Ubuntu 터미널에서 `uname -m`이 `aarch64`로 출력됐습니다.
2. 처음에는 `wget`이 `raw.githubusercontent.com`의 이름을 확인하지 못했습니다. `ip route`에서 게이트웨이 `192.168.64.1`을 확인했고, `ping -c 1 1.1.1.1`은 성공했습니다. `sudo resolvectl dns enp0s1 1.1.1.1`로 게스트의 DNS를 임시 변경했습니다. 변경 후 `getent ahostsv4 raw.githubusercontent.com`은 주소를 반환했지만 `wget` 재시도는 실패했습니다. 이 임시 변경은 영구 네트워크 설정으로 검증하지 않았습니다.
3. Ubuntu 패키지 저장소의 `sudo apt update`가 성공했고 `sudo apt install -y curl`로 `curl`을 설치했습니다.
4. `curl -I --connect-timeout 10 https://raw.githubusercontent.com`에서 HTTPS 응답 헤더를 확인했습니다. 같은 서버에서 공개된 `install-jazzy.sh`를 `curl -fL --retry 3`으로 VM에 내려받았고, VM에서 `bash -n install-jazzy.sh`가 오류 없이 끝났습니다.
5. `bash install-jazzy.sh`를 시작했습니다. Ubuntu `universe` 저장소를 활성화했고, `ros2-apt-source` 버전 `1.3.0-noble`을 설치했습니다. `apt update`에서 `packages.ros.org/ros2/ubuntu noble`의 ARM64 패키지 목록을 가져왔습니다.
6. Jazzy·RViz·Nav2·SLAM Toolbox·Gazebo 연동 패키지 설치에 필요한 파일 약 904MB를 내려받았습니다. 스크립트가 끝나며 `rviz2`, `nav2_bringup`, `slam_toolbox`의 설치 경로를 모두 `/opt/ros/jazzy`로 확인했고, 셸 프롬프트가 돌아왔습니다.
7. `source /opt/ros/jazzy/setup.bash` 후 `rviz2`를 실행했습니다. Ubuntu 데스크톱의 RViz 창에 격자가 표시됐고 `RViz is ready`를 확인했습니다. 로봇을 연결하기 전이라 TF 데이터 경고가 있었습니다. `Ctrl+C`로 종료했습니다.
8. 설치 후 `df -h /`은 34GB 중 14GB 사용, 약 18GB 여유(44%)를 표시했습니다. `free -h`는 메모리 3.8GiB 중 약 2.3GiB를 사용 가능으로 표시했습니다.
9. `ros2 launch nav2_bringup tb3_simulation_launch.py --show-args`에서 기본값 `headless=True`, `slam=False`를 확인했습니다. 기본 설정으로 예제 실행을 시도하자 Gazebo(`gz`), 로봇 생성(`create`), Nav2 컨테이너, RViz 프로세스가 시작됐습니다. `/map`, `/scan`, `/odom`, `/tf`, `/plan` 등의 토픽 이름을 `ros2 topic list`에서 확인했고 `/odom`과 `/clock`은 각각 발행자 1개로 나타났습니다.
10. 하지만 예제 RViz에 `Global Status: Error`가 표시됐고 Nav2 로그가 `map`/`odom` 프레임 변환을 계속 기다렸습니다. `timeout 12 ros2 topic echo /odom --once`에서는 메시지를 받지 못했습니다. 기본 예제의 로봇 위치·주행은 검증하지 못해 `Ctrl+C`로 종료했습니다. 종료 과정에서 응답하지 않은 Nav2·RViz 프로세스는 런처가 `SIGKILL`로 정리했습니다. 기본 예제는 SLAM이 꺼져 있으므로 이번 시도는 새 지도 작성 검증도 아닙니다.

## 검증 상태

- Ubuntu VM의 네트워크 연결, `curl` 다운로드, 공식 ROS apt 저장소 등록: **확인**
- ROS 2 Jazzy와 RViz·Nav2·SLAM Toolbox 패키지 설치, RViz 데스크톱 창 실행: **확인**
- 기본 TurtleBot3 예제의 프로세스 시작과 토픽 이름: **확인**. 실제 `/odom` 메시지, 유효한 TF, 로봇 주행: **미확인**
- 이 UTM VM에서의 SLAM 지도 작성·저장과 Nav2 목표 주행: **미검증**. Gazebo 시계·센서 메시지와 VM 자원 사용을 추가 진단해야 합니다.

`sudo` 비밀번호는 사용자가 UTM 창에 직접 입력했습니다. 이 기록에는 비밀번호를 저장하지 않습니다.
