# UTM Ubuntu 설치 진행 기록 — 2026-11-23

## 환경

- 호스트: Apple Silicon Mac, 메모리 8GB
- UTM `Linux` VM: QEMU ARM64, vCPU 4개, 메모리 4GB, 새 VirtIO 디스크 35GB
- 설치 이미지: Ubuntu 24.04.4 Desktop ARM64
- 설치 계정은 사용자가 Ubuntu 설치기에서 만들었습니다. 비밀번호는 UTM 창에서 직접 설정했고 이 기록에 저장하지 않습니다.

## 실제 관찰

1. Ubuntu 설치기에서 새 VM 디스크를 설치 대상으로 선택하고 `Asia/Seoul` 시간대를 확인했습니다.
2. 설치기가 `Copying files`, `Installing the system`, `Setting up the system` 순서로 이동했습니다.
3. `Setting up the system` 화면에서 게스트 시계가 23:22에 멈췄고, 완료 또는 재시작 안내가 나오지 않았습니다. VM 디스크 파일은 약 9.8GB까지 증가한 뒤 23:25:46부터 쓰기 시각이 바뀌지 않았습니다.
4. UTM의 재시작 버튼에서 저장되지 않은 변경 사항이 사라질 수 있다는 경고가 나타났습니다. 사용자가 리셋과 부팅 확인을 승인해 VM을 재시작했습니다.
5. 설치 ISO의 GRUB 메뉴에서 `Boot from next volume`을 선택하자 내부 디스크의 Ubuntu EFI 부팅 항목이 실행됐습니다. 기존 UTM 디스플레이 카드 `virtio-ramfb`에서는 화면이 검게 남았습니다.
6. 게스트가 UTM의 정상 종료 요청에 응답했습니다. VM을 끈 뒤 디스플레이 카드를 비가속 `virtio-gpu-pci`로 변경하고 같은 내부 디스크로 다시 부팅했습니다.
7. 설치된 Ubuntu 24.04.4의 로그인 화면과 데스크톱이 나타났습니다. 사용자가 UTM 창에서 직접 비밀번호를 입력해 로그인했고, Ubuntu 터미널도 열렸습니다.
8. 설치 ISO가 연결된 상태여서 재부팅 시 ISO GRUB 메뉴에서 `Boot from next volume`을 선택했습니다. UTM의 ISO 제거 작업은 이미지 영구 삭제 경고가 나와 취소했고, ISO 파일은 보존했습니다.

## 검증 상태

- Ubuntu 설치, 내부 디스크 부팅, 사용자 로그인, 데스크톱과 터미널 실행: **확인**
- ROS 2 Jazzy, RViz, SLAM Toolbox, Nav2: **UTM VM에서 미설치·미검증**
- 이전 Docker 실습 결과와 이 UTM 기록은 별개입니다.

ROS 2 설치와 AMR 예제의 실행 결과는 별도로 검증해 추가합니다.
