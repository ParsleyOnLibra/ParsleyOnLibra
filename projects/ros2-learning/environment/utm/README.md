# UTM의 Ubuntu 데스크톱에서 ROS 2 실행

상태: Ubuntu 24.04.4의 내부 디스크 부팅, ROS 2 Jazzy 설치와 RViz 데스크톱 창 실행을 확인했습니다. [설치·부팅 기록](../../evidence/2026-11-23-utm-install.md)과 [ROS 2 실행 기록](../../evidence/2026-11-24-utm-ros-install.md)을 참고하세요. TurtleBot3 예제는 시작됐지만 TF 오류가 남아 이 VM에서 지도 작성과 목표 주행은 미검증입니다.

이 경로는 Apple Silicon Mac의 UTM 가상 머신 안에서 Ubuntu 24.04 ARM64와 RViz 앱을 직접 실행합니다. Gazebo의 시뮬레이션 서버는 화면 없이 실행해 8GB Mac의 그래픽·메모리 부담을 줄입니다. 지도 작성에는 SLAM Toolbox, 목표 주행에는 Nav2를 사용합니다.

## 준비된 가상 머신

- UTM의 `Linux` VM: CPU 4개, 메모리 4GB, 새 가상 디스크 35GB
- Ubuntu 24.04.4 Desktop ARM64 설치 이미지
- 설치 중 사용자 계정을 생성했고 로그인과 터미널 실행을 확인했습니다.
- Ubuntu 계정 비밀번호는 사용자가 UTM 창에 직접 설정·입력했습니다. 로그인과 터미널 실행을 확인했습니다.
- 화면이 검게 남는 문제를 해결하기 위해 UTM 디스플레이 카드를 비가속 `virtio-gpu-pci`로 설정했습니다.

가상 디스크를 초기화하는 선택은 **새로 만든 35GB VM 디스크에만** 적용됐습니다. Mac 디스크에는 적용되지 않았습니다. 설치 ISO는 현재 연결된 상태입니다. VM 시작 시 ISO의 GRUB 메뉴가 나오면 `Boot from next volume`을 선택해 내부 Ubuntu 디스크로 부팅합니다. UTM 편집기의 ISO `제거`는 이미지 영구 삭제 경고를 표시해 취소했습니다.

## Ubuntu에서 ROS 2 설치

Ubuntu 터미널에서 아래처럼 공개된 스크립트를 내려받고 내용을 확인한 뒤 실행합니다. `sudo`가 요구하는 비밀번호는 UTM의 Ubuntu 창에 직접 입력합니다.

```bash
sudo apt update && sudo apt install -y curl
curl -fL --retry 3 -o "$HOME/install-jazzy.sh" https://raw.githubusercontent.com/ParsleyOnLibra/ParsleyOnLibra/main/projects/ros2-learning/environment/utm/install-jazzy.sh
less "$HOME/install-jazzy.sh"
bash "$HOME/install-jazzy.sh"
```

스크립트는 Ubuntu 24.04 ARM64 여부를 확인하고 공식 ROS apt 소스를 등록한 뒤 ROS 2 Jazzy Desktop, RViz, Nav2, SLAM Toolbox, Gazebo 연동 패키지와 UTM 게스트 도구를 설치합니다. 패키지 설치 뒤 아래 명령으로 RViz 앱 실행 여부를 확인합니다.

```bash
source /opt/ros/jazzy/setup.bash
rviz2
```

## AMR 예제 실행

같은 VM의 Ubuntu 터미널에서 다음 명령으로 지도 작성 예제를 시도할 수 있습니다. Gazebo 3D 창은 실행하지 않고 RViz 앱에서 지도, 로봇 위치, 경로를 봅니다. **아래 SLAM 옵션을 넣은 실행은 이 VM에서 아직 검증하지 않았습니다.** 먼저 `/clock`, `/odom`, `/scan`, `/tf`가 실제 메시지를 내는지 확인해야 합니다.

```bash
source /opt/ros/jazzy/setup.bash
LIBGL_ALWAYS_SOFTWARE=1 ros2 launch nav2_bringup tb3_simulation_launch.py slam:=True headless:=True
```

2026-11-24에 옵션 없는 기본 예제를 실행했을 때 프로세스와 토픽 이름은 나타났지만 `map`/`odom` TF가 없고 `/odom` 메시지를 받지 못했습니다. 이 상태에서는 목표 주행 성공이나 지도 생성을 주장할 수 없습니다. [실제 실행 기록](../../evidence/2026-11-24-utm-ros-install.md)에 관찰 내용을 남겼습니다. 이후 주행과 지도 저장 절차는 [Docker 실행 안내](../README.md)의 ROS 명령을 참고하되, `docker compose exec` 부분만 빼고 Ubuntu 터미널에서 실행합니다.

## 참고

- [ROS 2 Jazzy Ubuntu deb 설치 문서](https://github.com/ros2/ros2_documentation/blob/jazzy/source/Installation/Ubuntu-Install-Debs.rst)
- [ROS apt 소스 설정 문서](https://github.com/ros2/ros2_documentation/blob/jazzy/source/Installation/_Apt-Repositories.rst)
- [Nav2 Jazzy 빠른 시작](https://docs.nav2.org/jazzy/getting_started/quickstart/quickstart/)
- [UTM Linux 게스트 지원](https://docs.getutm.app/guest-support/linux/)
