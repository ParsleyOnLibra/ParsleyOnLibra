# 가상 AMR 배터리 토픽 QA 명세와 테스트

이 실습은 `std_msgs/Int16`의 배터리 백분율을 `/qa/battery_pct`로 받고, 검증 결과를 JSON 문자열로 `/qa/battery_status`에 발행한다. 실제 로봇·배터리 드라이버·유진로봇 제품과 무관하다. 20% 경계와 2초 타임아웃은 연습용 가상 정책이다.

| ID | 가상 요구사항 | 검증 케이스 |
| --- | --- | --- |
| B-01 | 정수 0~100만 유효하다. 0~19는 `LOW`, 20~100은 `NORMAL`이다. | `test_battery_boundary_and_range` |
| B-02 | 범위 밖·비정수는 `INVALID`로 보고하고 마지막 유효 배터리 값을 바꾸지 않는다. | `test_invalid_values_do_not_replace_last_valid` |
| B-03 | 시작 또는 마지막 유효 값 수신 후 2초 동안 유효 값이 없으면 `STALE`을 한 번 보고한다. 새 유효 값이 오면 정상·부족 상태로 복구한다. | `test_missing_data_becomes_stale_once`, `test_invalid_data_does_not_delay_timeout_and_valid_data_recovers` |
| B-04 | ROS 2 발행·구독에서 `LOW`·`INVALID`·`NORMAL`을 관찰하고 발행 중단 뒤 `STALE`, 재발행 뒤 복구를 관찰한다. | `test_pub_sub_invalid_timeout_and_recovery` |
| B-05 | 유효 배터리 값만 별도 AMR 가상 시뮬레이터에 전달한다. 19%는 미션 거부, 20%는 허용한다. | `test_19_percent_blocks_and_20_percent_allows_mission`, `test_invalid_battery_does_not_change_robot` |

## 실행

ROS 2 Jazzy와 `colcon`이 준비된 환경에서 저장소 루트 기준으로 실행한다.

```bash
source /opt/ros/jazzy/setup.bash
cd projects/ros2-learning
colcon build --packages-select battery_qa
source install/setup.bash
python3 -m unittest discover -s tests -v
```

두 터미널에서 `ros2 run battery_qa battery_monitor`, `ros2 run battery_qa battery_publisher`를 실행하면 상태 JSON을 확인할 수 있다. 발행기를 중단하고 2초 이상 기다리면 `STALE`, 다시 시작하면 복구 상태를 관찰할 수 있다. 실습용 발행 값은 `21, 20, 19, -1, 101, 50`을 반복한다.

## 해석 범위

- `battery_core.py`는 ROS 없이 검증할 수 있는 결정적 규칙이다. ROS 2 통신 테스트는 `rclpy`가 있을 때만 실행한다.
- `amr_adapter.py`는 이 저장소의 [가상 AMR 시뮬레이터](../../../amr-qa-lab/README.md)에 유효 값을 전달한다. 실제 로봇 통신 연결이 아니다.
- 이 테스트는 QoS 호환성, 실제 센서 지연, 무선 연결 장애, 물리적 주행 안전을 평가하지 않는다.
