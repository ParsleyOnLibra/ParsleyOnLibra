"""Run AI-suggested, specification-reviewed QA cases against a fictional flow."""

import argparse
import json
from pathlib import Path
import sys
from time import perf_counter

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from reward_sim import RewardFlow  # noqa: E402

ACCEPTED_CODES = {
    "INITIALIZED", "CONSENT_UPDATED", "OFFLINE", "ONLINE", "PENDING_CREDITED",
    "LOADED", "SHOWN", "REWARD_CREDITED", "REWARD_PENDING", "CLOSED",
}


def step(action, code, state, value=None):
    return {"action": action, "value": value, "accepted": code in ACCEPTED_CODES,
            "code": code, "state": state}


def case(case_id, requirements, title, steps, final):
    return {"id": case_id, "requirements": requirements, "title": title,
            "steps": steps, "final": final}


CASES = [
    case("TC-01", ["R-01", "R-02"], "초기화·동의 후 광고 노출", [
        step("initialize", "INITIALIZED", "EMPTY"),
        step("set_consent", "CONSENT_UPDATED", "EMPTY", "GRANTED"),
        step("load", "LOADED", "LOADED"),
        step("show", "SHOWN", "SHOWING"),
    ], {"state": "SHOWING", "impressions": 1, "credit_events": [], "pending": []}),
    case("TC-02", ["R-01"], "초기화 전 로드 거부", [
        step("set_consent", "CONSENT_UPDATED", "EMPTY", "GRANTED"),
        step("load", "NOT_INITIALIZED", "EMPTY"),
    ], {"state": "EMPTY", "impressions": 0, "credit_events": [], "pending": []}),
    case("TC-03", ["R-01"], "동의 거부 시 로드 거부", [
        step("initialize", "INITIALIZED", "EMPTY"),
        step("set_consent", "CONSENT_UPDATED", "EMPTY", "DENIED"),
        step("load", "CONSENT_REQUIRED", "EMPTY"),
    ], {"state": "EMPTY", "impressions": 0, "credit_events": [], "pending": []}),
    case("TC-04", ["R-01"], "로드 후 동의 철회 시 광고 무효화", [
        step("initialize", "INITIALIZED", "EMPTY"),
        step("set_consent", "CONSENT_UPDATED", "EMPTY", "GRANTED"),
        step("load", "LOADED", "LOADED"),
        step("set_consent", "CONSENT_UPDATED", "EMPTY", "DENIED"),
        step("show", "INVALID_STATE", "EMPTY"),
    ], {"state": "EMPTY", "impressions": 0, "credit_events": [], "pending": []}),
    case("TC-05", ["R-02"], "오프라인 로드 거부", [
        step("initialize", "INITIALIZED", "EMPTY"),
        step("set_consent", "CONSENT_UPDATED", "EMPTY", "GRANTED"),
        step("disconnect", "OFFLINE", "EMPTY"),
        step("load", "NETWORK_UNAVAILABLE", "EMPTY"),
    ], {"state": "EMPTY", "impressions": 0, "credit_events": [], "pending": []}),
    case("TC-06", ["R-02"], "로드 전 노출과 중복 노출 거부", [
        step("show", "INVALID_STATE", "EMPTY"),
        step("initialize", "INITIALIZED", "EMPTY"),
        step("set_consent", "CONSENT_UPDATED", "EMPTY", "GRANTED"),
        step("load", "LOADED", "LOADED"),
        step("show", "SHOWN", "SHOWING"),
        step("show", "INVALID_STATE", "SHOWING"),
    ], {"state": "SHOWING", "impressions": 1, "credit_events": [], "pending": []}),
    case("TC-07", ["R-03"], "노출 전 완료 콜백 거부", [
        step("complete", "INVALID_STATE", "EMPTY", "tx-7"),
    ], {"state": "EMPTY", "impressions": 0, "credit_events": [], "pending": []}),
    case("TC-08", ["R-03"], "정상 보상과 중복 콜백 차단", [
        step("initialize", "INITIALIZED", "EMPTY"),
        step("set_consent", "CONSENT_UPDATED", "EMPTY", "GRANTED"),
        step("load", "LOADED", "LOADED"),
        step("show", "SHOWN", "SHOWING"),
        step("complete", "REWARD_CREDITED", "SHOWING", "tx-8"),
        step("complete", "DUPLICATE_IGNORED", "SHOWING", "tx-8"),
    ], {"state": "SHOWING", "impressions": 1, "credit_events": ["tx-8"], "pending": []}),
    case("TC-09", ["R-04"], "오프라인 완료 후 연결 복구 시 한 번만 보상", [
        step("initialize", "INITIALIZED", "EMPTY"),
        step("set_consent", "CONSENT_UPDATED", "EMPTY", "GRANTED"),
        step("load", "LOADED", "LOADED"),
        step("show", "SHOWN", "SHOWING"),
        step("disconnect", "OFFLINE", "SHOWING"),
        step("complete", "REWARD_PENDING", "SHOWING", "tx-9"),
        step("complete", "DUPLICATE_IGNORED", "SHOWING", "tx-9"),
        step("reconnect", "PENDING_CREDITED", "SHOWING"),
        step("reconnect", "ONLINE", "SHOWING"),
    ], {"state": "SHOWING", "impressions": 1, "credit_events": ["tx-9"], "pending": []}),
    case("TC-10", ["R-05"], "완료 전 닫기에는 보상 없음", [
        step("initialize", "INITIALIZED", "EMPTY"),
        step("set_consent", "CONSENT_UPDATED", "EMPTY", "GRANTED"),
        step("load", "LOADED", "LOADED"),
        step("show", "SHOWN", "SHOWING"),
        step("close", "CLOSED", "CLOSED"),
        step("complete", "INVALID_STATE", "CLOSED", "tx-10"),
    ], {"state": "CLOSED", "impressions": 1, "credit_events": [], "pending": []}),
    case("TC-11", ["R-04", "R-05"], "오프라인 완료 뒤 닫아도 복구 시 보상", [
        step("initialize", "INITIALIZED", "EMPTY"),
        step("set_consent", "CONSENT_UPDATED", "EMPTY", "GRANTED"),
        step("load", "LOADED", "LOADED"),
        step("show", "SHOWN", "SHOWING"),
        step("disconnect", "OFFLINE", "SHOWING"),
        step("complete", "REWARD_PENDING", "SHOWING", "tx-11"),
        step("close", "CLOSED", "CLOSED"),
        step("reconnect", "PENDING_CREDITED", "CLOSED"),
    ], {"state": "CLOSED", "impressions": 1, "credit_events": ["tx-11"], "pending": []}),
    case("TC-12", ["R-03"], "거래 ID 누락 시 보상 거부", [
        step("initialize", "INITIALIZED", "EMPTY"),
        step("set_consent", "CONSENT_UPDATED", "EMPTY", "GRANTED"),
        step("load", "LOADED", "LOADED"),
        step("show", "SHOWN", "SHOWING"),
        step("complete", "INVALID_TXN", "SHOWING", ""),
    ], {"state": "SHOWING", "impressions": 1, "credit_events": [], "pending": []}),
]


class DuplicateCreditFlow(RewardFlow):
    """Intentional fault: a repeated completion writes a second credit event."""

    def command(self, action, value=None):
        result = super().command(action, value)
        if action == "complete" and result["code"] == "DUPLICATE_IGNORED" and value in self.credited:
            self.credit_events.append(value)
        return result


def run_case(test_case, flow_type):
    flow = flow_type()
    failures = []
    observed = []
    for index, expected in enumerate(test_case["steps"], 1):
        actual = flow.command(expected["action"], expected["value"])
        for key in ("accepted", "code", "state"):
            if actual[key] != expected[key]:
                failures.append(f"step {index} {key}: expected {expected[key]}, got {actual[key]}")
        observed.append({"expected": expected, "actual": actual})
    snapshot = flow.snapshot()
    for key, value in test_case["final"].items():
        if snapshot[key] != value:
            failures.append(f"final {key}: expected {value!r}, got {snapshot[key]!r}")
    if len(flow.events) != len(test_case["steps"]):
        failures.append("event count does not match command count")
    if [event["seq"] for event in flow.events] != list(range(1, len(flow.events) + 1)):
        failures.append("event sequence is not continuous")
    for index, (event, result) in enumerate(zip(flow.events, observed), 1):
        if event["code"] != result["actual"]["code"]:
            failures.append(f"event {index} code does not match command result")
    return {"id": test_case["id"], "requirements": test_case["requirements"],
            "title": test_case["title"], "status": "PASS" if not failures else "FAIL",
            "failures": failures, "steps": observed, "snapshot": snapshot, "events": flow.events}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mutation", action="store_true", help="Inject a duplicate reward defect")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    ids = [item["id"] for item in CASES]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate case ID")
    required_ids = {f"R-{index:02d}" for index in range(1, 6)}
    covered_ids = {req for item in CASES for req in item["requirements"]}
    if covered_ids != required_ids:
        raise ValueError(f"requirement coverage mismatch: {covered_ids ^ required_ids}")
    flow_type = DuplicateCreditFlow if args.mutation else RewardFlow
    start = perf_counter()
    results = [run_case(item, flow_type) for item in CASES]
    duration = perf_counter() - start
    report = {"sut": "fictional reward-ad state simulator", "mutation": args.mutation,
              "total": len(results), "passed": sum(x["status"] == "PASS" for x in results),
              "failed": sum(x["status"] == "FAIL" for x in results),
              "steps": sum(len(x["steps"]) for x in results),
              "duration_seconds": round(duration, 6),
              "requirements_covered": sorted(covered_ids), "cases": results}
    output = args.output or ROOT / "results" / ("mutation.json" if args.mutation else "latest.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{report['passed']}/{report['total']} passed; {report['steps']} steps; {duration:.4f}s; {output}")
    for result in results:
        if result["status"] == "FAIL":
            print(result["id"] + ": " + "; ".join(result["failures"]))
    if args.mutation:
        return 0 if report["failed"] >= 1 else 1
    return 1 if report["failed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
