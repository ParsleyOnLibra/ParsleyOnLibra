# ROS 2 학습 기록 — AMR QA 관점

시작일: 2026-10-29 · 상태: 기존 ROS 2 학습 기록과 Codex가 만든 배터리 QA 공개 초안

> **배터리 QA 단계 3~5는 본인 단독 수행 성과로 소개하지 않음.** 해당 코드, 테스트, 문서는 2026-11-23 Codex가 작성했고 CI에서 실행했습니다. 양종수 님은 아직 직접 이해하거나 재현했다고 확인하지 않았습니다. 이후 판단과 검증 기록은 출처를 구분해 추가합니다.

AMR QA 경험을 바탕으로 로봇 내부의 데이터 흐름을 관찰하고 문제를 재현하는 방법을 공부합니다. 이 공간은 학습 노트, 실습 코드, 실행 증거, 테스트 설계와 문제 해결 과정을 함께 보관합니다.

## 현재 기록

- [001 · ROS 2 기본 개념과 AMR QA](notes/001-concepts.md): 개념 설명, 확인 질문과 참고 답안. 사용자의 직접 답변은 아직 기록되지 않았습니다.
- [실습 기록 양식](templates/lab-record.md)
- [Apple Silicon Docker 실행 환경](environment/README.md): ROS 2 Jazzy, Gazebo, Nav2, SLAM Toolbox, RViz 실행 절차
- [UTM Ubuntu 데스크톱 실행 환경](environment/utm/README.md): 별도 환경의 설정 초안. UTM에서의 실행은 확인하지 않았습니다.
- [2026-11-18 실행 증거](evidence/2026-11-18-environment.md): 부분 지도 생성·저장과 목표 주행 결과
- [배터리 토픽 QA 명세·케이스](docs/BATTERY_QA.md): 20% 경계, 입력 오류, 메시지 중단·복구, 가상 AMR 연계
- [2026-11-23 배터리 QA 실행 증거](evidence/2026-11-23-battery-qa.md): ROS 2 Jazzy CI의 패키지 빌드·7개 테스트 통과와 로그

## 학습 초안 산출물

| 단계 | 주제 | 남길 산출물 | 상태 |
| --- | --- | --- | --- |
| 1 | 노드·토픽·서비스·액션 | 개념 노트, 확인 질문과 참고 답안 | 문서 완료; 사용자 이해도 별도 |
| 2 | 실행 환경과 기본 예제 | Docker 설정, Gazebo·SLAM 실행, 부분 지도·목표 주행 증거 | 2026-11-18 실행 확인 |
| 3 | Python 배터리 Publisher / Subscriber | `battery_qa` ROS 2 패키지와 실행 명령 | Codex 구현·CI 확인, 사용자 재현 전 |
| 4 | 통신과 오류 상황 검증 | 19·20% 경계, 잘못된 값, 메시지 중단·복구 테스트 | Codex 구현·CI 확인, 사용자 재현 전 |
| 5 | AMR QA 테스트 랩 연계 | 유효 배터리 이벤트를 가상 AMR 상태 시뮬레이터에 전달 | Codex 구현·CI 확인, 사용자 재현 전 |

## 재현

ROS 2 Jazzy에서 다음 명령을 실행합니다. CI는 [ROS 2 battery QA 실행 결과](https://github.com/ParsleyOnLibra/ParsleyOnLibra/actions/runs/45151500094)로 확인할 수 있습니다.

```bash
source /opt/ros/jazzy/setup.bash
cd projects/ros2-learning
colcon build --packages-select battery_qa
source install/setup.bash
python3 -m unittest discover -s tests -v
```

두 터미널에서 `ros2 run battery_qa battery_monitor`와 `ros2 run battery_qa battery_publisher`를 실행할 수 있습니다. 자세한 토픽·기대 결과는 [배터리 QA 문서](docs/BATTERY_QA.md)에 있습니다.

## 기록·공개 원칙

- 학습할 때마다 노트와 해당 작업 산출물을 같은 변경에 반영하고 포트폴리오의 진행 상태를 갱신합니다.
- 코드는 `src/`, 테스트는 `tests/`, 실행 기록은 `evidence/`에 실제 산출물이 생길 때 추가합니다.
- 실행 환경, 명령, 예상 결과와 실제 결과, 오류와 해결 과정, 남은 질문을 기록합니다.
- 작성한 예제와 실제 실행 검증을 구분합니다. 실행하지 않은 결과를 성공으로 표시하지 않습니다.
- 직접 만든 공개 가능한 자료를 올립니다. 개인정보·인증정보·회사 내부 자료는 제외하고, 외부 자료는 출처 링크와 직접 정리한 설명으로 남깁니다.
- 큰 rosbag·영상은 저장 방식과 용량을 정한 뒤 연결하고, 재현에 필요한 설정·요약·보관 위치를 기록합니다.

## 공식 학습 자료

- [ROS 2 문서](https://docs.ros.org/)
- [공식 문서 원본](https://github.com/ros2/ros2_documentation)

현재 실습 배포판은 ROS 2 Jazzy이며 Apple Silicon macOS의 ARM64 Ubuntu 24.04 Docker 컨테이너에서 실행했습니다. 지도는 시작점 주변의 부분 지도입니다.

배터리 패키지와 테스트는 2026-11-23 Codex가 작성했고 GitHub Actions의 ROS 2 컨테이너에서 검증했습니다. 사용자가 별도로 직접 실행하거나 이해도 질문에 답한 기록은 아직 없습니다. UTM VM, 실제 배터리 센서, 장애물 회피·도킹과 실물 로봇 검증은 이 포트폴리오 범위에 포함하지 않습니다.
