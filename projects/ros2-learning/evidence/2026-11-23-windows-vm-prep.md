# 2026-11-23 · Windows 독립 실행 환경 준비 기록

## 작성·확인한 것

- Windows의 Intel/AMD 64비트 PC를 위한 Ubuntu 24.04 AMD64 VM 설치 절차를 작성했다.
- 공식 ROS apt 소스와 ROS 2 Jazzy Desktop, Nav2, SLAM Toolbox, Gazebo 연동 패키지를 설치하는 `environment/windows-vm/install-jazzy-amd64.sh`를 작성했다.
- Mac 작업 공간에서 `bash -n`으로 스크립트의 셸 문법을 확인했다. 이 검사는 패키지 설치 성공 여부를 확인하지 않는다.
- 포트폴리오의 ROS 2 프로젝트 페이지를 작성하고 로컬 상대 링크의 대상 파일 존재 여부를 확인했다.

## 아직 확인하지 못한 것

- 이 작업 세션에서 Windows PC 화면에 접근할 수 없었다. Windows의 버전·CPU·RAM·디스크 여유 공간은 아직 받지 못했다.
- 따라서 VirtualBox 설치, Ubuntu VM 생성, ROS 2 패키지 설치, RViz와 Gazebo 실행, 지도 작성·저장 및 목표 주행은 **Windows에서 실행하지 않았다**.
- Mac Docker의 기존 성공 결과는 Windows VM의 성공 증거로 사용하지 않는다.

## 다음 확인 순서

Windows PC 사양 확인 → VM 자원 결정 → Ubuntu 설치 → ROS 2 설치 → RViz 창 확인 → `/map`·`/scan` 확인 → 지도 저장 → Nav2 목표 주행 → 결과·오류 기록.
