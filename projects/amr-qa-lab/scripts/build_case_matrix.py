"""Render the reviewed case definitions as a readable Markdown catalog."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
cases = json.loads((ROOT / "cases" / "test_cases.json").read_text(encoding="utf-8"))
lines = [
    "# 테스트케이스 목록",
    "",
    "모든 케이스는 독립된 가상 로봇에서 시작한다. 기본 사전 조건은 `IDLE`, 지도 있음, 경로 유효, 배터리 50%, 도크 있음이다. 바뀐 조건은 아래 표에 표시했다. 상세 입력과 예상 반환값은 [JSON 원본](../cases/test_cases.json)에 있다.",
    "",
    "| ID | 요구사항 | 우선순위 | 설계 기법 | 목적·변경한 사전 조건 | 절차 → 예상 결과 |",
    "| --- | --- | --- | --- | --- | --- |",
]
for case in cases:
    setup = ", ".join(f"{key}={value}" for key, value in case.get("setup", {}).items()) or "기본값"
    steps = "<br>".join(
        f"{index}. `{step['command']}`" + (f"({step['value']})" if "value" in step else "")
        + f" → `{step['expect']['code']}`, `{step['expect']['state']}`"
        for index, step in enumerate(case["steps"], 1)
    )
    lines.append(f"| {case['id']} | {', '.join(case['requirements'])} | {case['priority']} | {case['technique']} | {case['title']}; {setup} | {steps} |")
lines += ["", "`PASS`는 기록된 모든 단계의 승인 여부, 결과 코드, 상태가 예상값과 일치하고 명령 로그의 순번이 연속임을 뜻한다. 실행 결과는 [최신 보고서](../results/latest.json)에서 확인할 수 있다.", ""]
(ROOT / "docs" / "TEST_CASES.md").write_text("\n".join(lines), encoding="utf-8")
print(f"Rendered {len(cases)} cases to docs/TEST_CASES.md")
