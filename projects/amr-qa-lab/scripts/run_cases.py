"""Execute independent, data-driven black-box QA cases and write a report."""

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from amr_sim import Robot  # noqa: E402


def run_case(case: dict, robot_class=Robot) -> dict:
    robot = robot_class(**case.get("setup", {}))
    observed = []
    failures = []
    for index, step in enumerate(case["steps"], 1):
        result = robot.command(step["command"], step.get("value"))
        expected = step["expect"]
        for field in ("accepted", "code", "state"):
            if result[field] != expected[field]:
                failures.append(f"step {index} {field}: expected {expected[field]!r}, got {result[field]!r}")
        observed.append({"command": step["command"], "value": step.get("value"),
                         "expected": expected, "actual": result})
    if len(robot.events) != len(case["steps"]):
        failures.append("event count does not equal command count")
    if [event["seq"] for event in robot.events] != list(range(1, len(robot.events) + 1)):
        failures.append("event sequence is not strictly increasing")
    return {"id": case["id"], "title": case["title"],
            "requirements": case["requirements"], "technique": case["technique"],
            "priority": case["priority"], "status": "PASS" if not failures else "FAIL",
            "failures": failures, "steps": observed, "events": robot.events}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", type=Path, default=ROOT / "cases" / "test_cases.json")
    parser.add_argument("--output", type=Path, default=ROOT / "results" / "latest.json")
    args = parser.parse_args()
    cases = json.loads(args.cases.read_text(encoding="utf-8"))
    ids = [case["id"] for case in cases]
    if len(ids) != len(set(ids)):
        raise ValueError("case IDs must be unique")
    results = [run_case(case) for case in cases]
    report = {"project": "AMR Mission and Docking QA Lab", "sut": "fictional deterministic simulator",
              "total": len(results), "passed": sum(x["status"] == "PASS" for x in results),
              "failed": sum(x["status"] == "FAIL" for x in results), "cases": results}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{report['passed']}/{report['total']} cases passed; report: {args.output}")
    for result in results:
        if result["status"] == "FAIL":
            print(result["id"] + ": " + "; ".join(result["failures"]))
    return 1 if report["failed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
