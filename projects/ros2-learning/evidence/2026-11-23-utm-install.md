# UTM Ubuntu 설치 진행 기록 — 2026-11-23

## 환경

- 호스트: Apple Silicon Mac, 메모리 8GB
- UTM `Linux` VM: QEMU ARM64, vCPU 4개, 메모리 4GB, 새 VirtIO 디스크 35GB
- 설치 이미지: Ubuntu 24.04.4 Desktop ARM64
- 설치 계정: `yang`, 호스트 이름 `amr-ros2`. 비밀번호는 사용자가 UTM 창에서 직접 설정했고 이 기록에 저장하지 않습니다.

## 실제 관찰

1. Ubuntu 설치기에서 새 VM 디스크를 설치 대상으로 선택하고 `Asia/Seoul` 시간대를 확인했습니다.
2. 설치기가 `Copying files`, `Installing the system`, `Setting up the system` 순서로 이동했습니다.
3. `Setting up the system` 화면에서 게스트 시계가 23:22에 멈췄고, 완료 또는 재시작 안내가 나오지 않았습니다. VM 디스크 파일은 약 9.8GB까지 증가한 뒤 23:25:46부터 쓰기 시각이 바뀌지 않았습니다.
4. UTM의 재시작 버튼을 누르자 저장되지 않은 변경 사항이 사라질 수 있다는 경고가 나타났습니다. 경고 화면에서 사용자의 선택을 기다리고 있습니다.

## 검증 상태

- Ubuntu 설치 완료 및 새 디스크 부팅: **미확인**
- ROS 2 Jazzy, RViz, SLAM Toolbox, Nav2: **UTM VM에서 미설치·미검증**
- 이전 Docker 실습 결과와 이 UTM 기록은 별개입니다.

설치가 재개되거나 부팅 결과가 확인되면 이 기록에 실제 결과를 추가합니다.
