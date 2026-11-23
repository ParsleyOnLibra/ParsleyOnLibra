# 2026-11-23 · ROS 2 배터리 토픽 QA 실행 기록

## 실행 환경과 출처

- GitHub Actions: [ROS 2 battery QA 성공 실행 #45151500094](https://github.com/ParsleyOnLibra/ParsleyOnLibra/actions/runs/45151500094)
- 검증 커밋: `075de70ba495ef5de1f98eed13c7aaf0d7fa5027`
- 컨테이너: Docker Official Image `ros:jazzy-ros-base`, GitHub `ubuntu-24.04` runner
- 명령: ROS 환경 설정 → `colcon build --packages-select battery_qa` → `ros2 pkg executables battery_qa` → `python3 -m unittest discover -s tests -v`

## 실제 결과

- `battery_qa` 패키지 1개 빌드 완료. `battery_monitor`와 `battery_publisher` 실행 명령 등록 확인.
- `unittest` **7개 통과, 건너뛰기 0개**. 순수 규칙 4개, 가상 AMR 연계 2개, 실제 `rclpy` 발행·구독 통신 1개다.
- ROS 2 통신 로그에서 `19 → LOW`, `101 → INVALID`, `20 → NORMAL`, 발행 중단 후 `STALE`, 재발행 후 `NORMAL`을 확인했다.
- 통신 테스트는 같은 컨테이너 안의 가상 토픽과 노드를 사용했다. 실제 배터리 센서나 실물 로봇은 연결하지 않았다.

## 오류와 수정

첫 CI 실행은 테스트 전에 `/opt/ros/jazzy/setup.bash`와 셸의 `set -u`가 충돌해 실패했다. [실패 실행 #45150931584](https://github.com/ParsleyOnLibra/ParsleyOnLibra/actions/runs/45150931584)에서 `AMENT_TRACE_SETUP_FILES: unbound variable`을 확인했다. 환경 설정 앞의 `-u`를 제거하고, 이미지에 이미 설치된 의존성을 다시 설치하던 단계를 없앤 뒤 재실행했다.

## 해석 범위

이 결과는 ROS 2 Jazzy 컨테이너의 가상 토픽 흐름과 가상 AMR 상태 시뮬레이터의 배터리 경계를 검증한다. 실제 로봇, 무선 네트워크, 센서, 현장 안전성은 검증하지 않는다. 기존 Docker SLAM·Nav2 실행 결과는 [2026-11-18 환경 기록](2026-11-18-environment.md)에 별도로 있다.
