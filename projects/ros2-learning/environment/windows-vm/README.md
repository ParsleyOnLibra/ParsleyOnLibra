# Windows PC에서 독립 실행하는 ROS 2 AMR 실습 환경

상태: Windows용 설치 절차와 스크립트 작성. Windows PC의 VM 생성, ROS 2 설치, RViz 실행, 지도 작성·주행은 아직 검증 전입니다.

Mac의 UTM VM은 Apple Silicon용 Ubuntu ARM64입니다. Windows PC가 일반적인 Intel/AMD 64비트 CPU라면 Ubuntu 24.04 **AMD64** 데스크톱 VM을 새로 만들고, 공개 ROS 2 코드와 지도 파일을 가져옵니다. 이 VM은 Windows PC에서 독립적으로 실행되므로 Mac을 켜 둘 필요가 없습니다.

## 1. Windows PC와 설치 파일 확인

Windows **설정 → 시스템 → 정보**에서 프로세서와 설치된 RAM을 확인합니다. 아래 절차는 **Intel/AMD 64비트 PC**를 기준으로 합니다. Windows on ARM PC라면 Ubuntu 이미지와 VM 설정을 다시 선택해야 합니다.

- [Oracle VirtualBox Windows 호스트 설치 파일](https://www.virtualbox.org/wiki/Downloads)
- [Ubuntu 24.04 LTS AMD64 데스크톱 이미지](https://ubuntu.com/download/alternative-downloads): `24.04.5.1 LTS`의 Intel/AMD 64비트 버전을 선택합니다.

VirtualBox는 Windows에서 Ubuntu 데스크톱 VM을 실행할 수 있고, Guest Additions를 설치하면 창 크기 조절과 일부 3D 그래픽 가속을 사용할 수 있습니다. 실제 RViz·Gazebo 성능은 PC 사양과 드라이버에 따라 검증해야 합니다.

## 2. Ubuntu VM 생성

VirtualBox에서 **새로 만들기**를 선택하고 Ubuntu ISO를 지정합니다. 사용자 이름과 비밀번호는 Ubuntu 설치 화면에서 직접 정하도록 **무인 설치 건너뛰기**를 선택합니다. 아래 자원 값은 호스트 RAM이 16GB 이상일 때의 시작값이며, PC 사양을 확인한 뒤 조정합니다.

| 항목 | 시작값 |
| --- | --- |
| 이름 | `amr-ros2-jazzy` |
| 게스트 OS | Ubuntu 24.04 64비트, AMD64 |
| CPU | 4 vCPU |
| 메모리 | 8GB (호스트 RAM 16GB 이상일 때) |
| 가상 디스크 | 60GB, 동적 할당 |
| 그래픽 | VMSVGA, 비디오 메모리 128MB, 3D 가속 사용 |

Ubuntu를 설치할 때 **디스크 지우기**는 새로 만든 *가상 디스크*에만 적용합니다. 설치가 끝나면 ISO를 분리하고 재부팅합니다. 창 크기 변경이나 3D 가속이 동작하지 않으면 [VirtualBox Guest Additions](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/guestadditions.html)를 설치한 뒤 다시 확인합니다.

## 3. Ubuntu 안에 ROS 2 Jazzy 설치

Ubuntu 터미널에서 다음 명령으로 이 저장소의 설치 스크립트를 내려받고 내용을 확인한 뒤 실행합니다. `sudo` 비밀번호는 Ubuntu 창에 직접 입력합니다.

```bash
sudo apt update && sudo apt install -y curl
curl -fL --retry 3 -o "$HOME/install-jazzy-amd64.sh" https://raw.githubusercontent.com/ParsleyOnLibra/ParsleyOnLibra/main/projects/ros2-learning/environment/windows-vm/install-jazzy-amd64.sh
less "$HOME/install-jazzy-amd64.sh"
bash "$HOME/install-jazzy-amd64.sh"
```

스크립트는 Ubuntu 24.04 AMD64를 확인하고 공식 ROS apt 소스를 등록합니다. ROS 2 Jazzy Desktop, RViz, Nav2, SLAM Toolbox 및 Gazebo 연동 패키지를 설치합니다. 설치 후 새 Ubuntu 터미널에서 `rviz2`를 실행해 앱 창이 열리는지 확인합니다.

## 4. 지도 작성과 목표 주행

Ubuntu 터미널에서 아래 명령으로 Gazebo 시뮬레이션 서버, SLAM Toolbox, Nav2, RViz를 시작합니다. 첫 실행은 Gazebo 3D 창 없이 확인합니다.

```bash
source /opt/ros/jazzy/setup.bash
ros2 launch nav2_bringup tb3_simulation_launch.py slam:=True headless:=True
```

다른 Ubuntu 터미널에서 `/map`, `/scan`, `/odom` 토픽을 확인합니다.

```bash
source /opt/ros/jazzy/setup.bash
ros2 topic list
ros2 lifecycle get /slam_toolbox
```

RViz의 **Nav2 Goal** 도구로 로봇을 이동시킨 뒤 지도를 저장합니다.

```bash
mkdir -p "$HOME/ros2_maps"
ros2 run nav2_map_server map_saver_cli -f "$HOME/ros2_maps/amr_map" --ros-args -p save_map_timeout:=10.0
```

저장한 지도로 다시 주행할 때는 앞선 시뮬레이션을 종료한 뒤 다음 명령으로 시작합니다. RViz에서 **2D Pose Estimate**로 로봇의 시작 위치를 지정하고 **Nav2 Goal**을 보냅니다.

```bash
ros2 launch nav2_bringup tb3_simulation_launch.py slam:=False map:="$HOME/ros2_maps/amr_map.yaml" headless:=True
```

RViz 화면이 검게 보이거나 OpenGL 오류가 나면 `LIBGL_ALWAYS_SOFTWARE=1 rviz2`로 소프트웨어 렌더링을 시험합니다. 실제 3D Gazebo 창은 기본 주행이 성공한 후 `headless:=False`로 별도 확인합니다.

## 5. 실행 증거와 포트폴리오 반영

Windows PC에서 실제 실행한 날짜, Windows·VirtualBox·Ubuntu·ROS 버전, PC/VM 자원, 실행 명령, `/map`·주행 결과, 오류와 해결 과정을 `evidence/`에 기록합니다. 지도 파일과 화면 캡처는 개인정보나 회사 자료가 없는지 확인한 후 공개 저장소에 올립니다. [Mac Docker 실행 증거](../../evidence/2026-11-18-environment.md)는 별도 환경에서 검증한 결과이며 Windows 검증 결과로 간주하지 않습니다.

## 공식 자료

- [Ubuntu의 VirtualBox 7 설치 튜토리얼](https://ubuntu.com/tutorials/how-to-run-ubuntu-desktop-on-a-virtual-machine-using-virtualbox)
- [VirtualBox 가상 머신 그래픽 설정](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/working-with-vms.html)
- [ROS 2 Jazzy Ubuntu 설치](https://github.com/ros2/ros2_documentation/blob/jazzy/source/Installation/Ubuntu-Install-Debs.rst)
- [Nav2 Jazzy 빠른 시작](https://docs.nav2.org/jazzy/getting_started/quickstart/quickstart/)
