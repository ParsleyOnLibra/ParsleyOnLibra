# 테스트케이스 목록

모든 케이스는 독립된 가상 로봇에서 시작한다. 기본 사전 조건은 `IDLE`, 지도 있음, 경로 유효, 배터리 50%, 도크 있음이다. 바뀐 조건은 아래 표에 표시했다. 상세 입력과 예상 반환값은 [JSON 원본](../cases/test_cases.json)에 있다.

| ID | 요구사항 | 우선순위 | 설계 기법 | 목적·변경한 사전 조건 | 절차 → 예상 결과 |
| --- | --- | --- | --- | --- | --- |
| TC-MIS-01 | R-01, R-02 | P0 | boundary value | 배터리 20%에서 미션 승인; battery=20 | 1. `start_mission` → `MISSION_STARTED`, `MOVING` |
| TC-MIS-02 | R-01 | P0 | decision table | 지도가 없으면 미션 거부; map_loaded=False | 1. `start_mission` → `MAP_MISSING`, `IDLE` |
| TC-MIS-03 | R-01 | P0 | decision table | 경로가 유효하지 않으면 미션 거부; route_valid=False | 1. `start_mission` → `ROUTE_INVALID`, `IDLE` |
| TC-MIS-04 | R-01 | P1 | state transition | 이동 중 중복 미션 거부; 기본값 | 1. `start_mission` → `MISSION_STARTED`, `MOVING`<br>2. `start_mission` → `INVALID_STATE`, `MOVING` |
| TC-BAT-01 | R-02 | P0 | boundary value | 배터리 19%에서 미션 거부; battery=19 | 1. `start_mission` → `BATTERY_LOW`, `IDLE` |
| TC-BAT-02 | R-02 | P1 | boundary value | 배터리 21%에서 미션 승인; battery=21 | 1. `start_mission` → `MISSION_STARTED`, `MOVING` |
| TC-BAT-03 | R-02 | P1 | equivalence partition | 배터리 0%에서 미션 거부; battery=0 | 1. `start_mission` → `BATTERY_LOW`, `IDLE` |
| TC-BAT-04 | R-06 | P1 | boundary value | 배터리 범위 밖 입력 거부; 기본값 | 1. `set_battery`(-1) → `INVALID_BATTERY`, `IDLE`<br>2. `set_battery`(101) → `INVALID_BATTERY`, `IDLE`<br>3. `start_mission` → `MISSION_STARTED`, `MOVING` |
| TC-OBS-01 | R-03 | P0 | state transition | 장애물 감지 후 해제 시 이동 재개; 기본값 | 1. `start_mission` → `MISSION_STARTED`, `MOVING`<br>2. `detect_obstacle` → `OBSTACLE_DETECTED`, `BLOCKED`<br>3. `clear_obstacle` → `OBSTACLE_CLEARED`, `MOVING` |
| TC-OBS-02 | R-03 | P1 | state transition | 감지 전 장애물 해제 명령 거부; 기본값 | 1. `start_mission` → `MISSION_STARTED`, `MOVING`<br>2. `clear_obstacle` → `INVALID_STATE`, `MOVING` |
| TC-OBS-03 | R-03 | P1 | state transition | 막힌 상태에서 중복 감지 거부; 기본값 | 1. `start_mission` → `MISSION_STARTED`, `MOVING`<br>2. `detect_obstacle` → `OBSTACLE_DETECTED`, `BLOCKED`<br>3. `detect_obstacle` → `INVALID_STATE`, `BLOCKED` |
| TC-EST-01 | R-04 | P0 | state transition | 비상정지 중 미션·도킹·재개 거부; 기본값 | 1. `start_mission` → `MISSION_STARTED`, `MOVING`<br>2. `press_estop` → `ESTOP_PRESSED`, `ESTOP`<br>3. `start_mission` → `ESTOP_ACTIVE`, `ESTOP`<br>4. `request_dock` → `ESTOP_ACTIVE`, `ESTOP`<br>5. `clear_obstacle` → `ESTOP_ACTIVE`, `ESTOP` |
| TC-EST-02 | R-04 | P0 | state transition | 비상정지 해제 후 자동 재개 없음; 기본값 | 1. `start_mission` → `MISSION_STARTED`, `MOVING`<br>2. `press_estop` → `ESTOP_PRESSED`, `ESTOP`<br>3. `release_estop` → `ESTOP_RELEASED`, `IDLE` |
| TC-EST-03 | R-04 | P2 | state transition | 비상정지 아닌 상태에서 해제 명령 거부; 기본값 | 1. `release_estop` → `INVALID_STATE`, `IDLE` |
| TC-DOC-01 | R-05 | P0 | state transition | 도킹 성공 시 충전 상태; 기본값 | 1. `request_dock` → `DOCKING_STARTED`, `DOCKING`<br>2. `dock_success` → `DOCKING_SUCCEEDED`, `CHARGING` |
| TC-DOC-02 | R-05 | P0 | state transition | 도킹 타임아웃 시 장애 상태; 기본값 | 1. `request_dock` → `DOCKING_STARTED`, `DOCKING`<br>2. `dock_timeout` → `DOCKING_TIMED_OUT`, `FAULT` |
| TC-DOC-03 | R-05 | P1 | state transition | 타임아웃 후 성공 신호 거부; 기본값 | 1. `request_dock` → `DOCKING_STARTED`, `DOCKING`<br>2. `dock_timeout` → `DOCKING_TIMED_OUT`, `FAULT`<br>3. `dock_success` → `INVALID_STATE`, `FAULT` |
| TC-DOC-04 | R-05 | P1 | decision table | 도크가 없으면 요청 거부; dock_available=False | 1. `request_dock` → `DOCK_UNAVAILABLE`, `IDLE` |
| TC-DOC-05 | R-05 | P1 | state transition | 이동 중 도킹 요청 가능; 기본값 | 1. `start_mission` → `MISSION_STARTED`, `MOVING`<br>2. `request_dock` → `DOCKING_STARTED`, `DOCKING` |
| TC-FLT-01 | R-05 | P1 | state transition | 도킹 장애 초기화 후 대기 상태; 기본값 | 1. `request_dock` → `DOCKING_STARTED`, `DOCKING`<br>2. `dock_timeout` → `DOCKING_TIMED_OUT`, `FAULT`<br>3. `reset_fault` → `FAULT_RESET`, `IDLE` |

`PASS`는 기록된 모든 단계의 승인 여부, 결과 코드, 상태가 예상값과 일치하고 명령 로그의 순번이 연속임을 뜻한다. 실행 결과는 [최신 보고서](../results/latest.json)에서 확인할 수 있다.
