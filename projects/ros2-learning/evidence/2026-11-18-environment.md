# 2026-11-18 · ROS 2 가상 AMR 환경 실행 기록

## 환경

- 호스트: Apple Silicon macOS 26.4.1, 메모리 8GB, Docker Desktop 29.4.2
- 컨테이너: Ubuntu 24.04 ARM64, ROS 2 Jazzy, Gazebo Sim 8.15.0
- 구성: Nav2, SLAM Toolbox, TurtleBot3 예제, RViz, Xvfb/noVNC
- Docker 할당 메모리: 약 3.8GiB. SLAM 실행 중 관측한 컨테이너 사용량은 약 0.8~1.2GiB였으며 측정 시점에 따라 달랐습니다.

## 실제 확인한 순서와 결과

1. `docker compose build` 성공. 이미지 `amr-ros2-jazzy:local` 생성.
2. `docker compose up -d` 성공. `http://127.0.0.1:6080/vnc.html`이 HTTP 200을 반환했고, 가상 데스크톱에서 RViz 화면을 캡처했습니다: [rviz-slam.png](rviz-slam.png).
3. `bash environment/run-slam.sh`로 Gazebo·Nav2·SLAM Toolbox·RViz 시작. `/map`, `/scan`, `/odom`, `/tf`, `/plan` 토픽을 확인했고 `ros2 lifecycle get /slam_toolbox`는 `active [3]`을 반환했습니다.
4. `/map` 메시지는 해상도 0.05m, 크기 111×102셀을 보고했습니다. 시작점 주변의 부분 지도이며 전체 공간 지도는 아닙니다.
5. `/navigate_to_pose` 목표 `(0.5, 0.0)`을 보냈고 액션 결과가 `error_code: 0`, `SUCCEEDED`였습니다. 주행 전·후 지도를 각각 `amr_initial_map.*`, `amr_map.*`로 저장했습니다. 두 PGM 파일의 SHA-1이 같아 이 짧은 주행으로 지도 범위가 넓어졌다는 증거는 얻지 못했습니다.
6. `bash environment/run-navigation.sh`로 저장 지도 기반 모드를 시작했습니다. `/map_server`, `/amcl`, `/bt_navigator`의 `active [3]`을 확인하고 `/initialpose`를 `(0, 0)`으로 발행했습니다. `/amcl_pose`에서 `(0, 0)`을 확인한 뒤 같은 목표 `(0.5, 0.0)`이 `SUCCEEDED`로 끝났습니다.

## 재현에 필요한 명령

`environment/README.md`에 시작·목표 주행·지도 저장·지도 재사용 명령을 적었습니다. 지도 저장 시 기본 2초 대기에서 한 번 실패했으며 `--ros-args -p save_map_timeout:=10.0`으로 성공했습니다.

## 확인 범위

- Gazebo의 3D 창은 메모리와 그래픽 부담을 줄이기 위해 실행하지 않았습니다. 물리·센서 시뮬레이션 서버와 RViz는 실행했습니다.
- `amr_map.*`는 0.5m 짧은 이동으로 만든 부분 지도입니다. 참고 영상의 큰 공간을 재현한 지도나 사용자 정의 AMR 모델은 아직 만들지 않았습니다. 2026-11-24에 영상을 다시 확인했지만 원본 프로그램의 ROS 2 사용 여부를 보여 주는 화면 증거는 없었습니다. 이 실습의 ROS 2 기술 스택은 원본 영상과 별개입니다.
- 장애물 회피·도킹·배터리·관제 UI 테스트는 이번 환경 설치에서 실행하지 않았습니다.
- 실제 로봇 또는 회사 제품에 대한 검증 결과가 아닙니다.
