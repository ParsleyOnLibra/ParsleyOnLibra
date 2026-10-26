"""Controlled fault injection to check whether the QA cases catch key defects.

These are synthetic mutations, not defects discovered in a real robot.
"""

import json
from pathlib import Path
from run_cases import ROOT, Robot, run_case


class OffByOneBattery(Robot):
    def command(self, action, value=None):
        if action == "start_mission" and self.battery == 20:
            self.battery = 19
        return super().command(action, value)


class UnsafeEstopRelease(Robot):
    def command(self, action, value=None):
        was_estop = self.state == "ESTOP"
        result = super().command(action, value)
        if action == "release_estop" and was_estop:
            self.state = "MOVING"
            result["state"] = "MOVING"
            self.events[-1]["to"] = "MOVING"
        return result


class FalseDockSuccess(Robot):
    def command(self, action, value=None):
        if action == "dock_timeout" and self.state == "DOCKING":
            result = super().command("dock_success", value)
            self.events[-1]["action"] = action
            return result
        return super().command(action, value)


def main():
    cases = json.loads((ROOT / "cases" / "test_cases.json").read_text(encoding="utf-8"))
    mutations = [
        ("battery_threshold_21_instead_of_20", OffByOneBattery),
        ("estop_release_resumes_mission", UnsafeEstopRelease),
        ("dock_timeout_reported_as_success", FalseDockSuccess),
    ]
    results = []
    for name, robot_class in mutations:
        caught_by = [case["id"] for case in cases if run_case(case, robot_class)["status"] == "FAIL"]
        results.append({"mutation": name, "caught": bool(caught_by), "caught_by": caught_by})
    output = ROOT / "results" / "mutations.json"
    output.write_text(json.dumps({"note": "Controlled injected faults; not real product defects", "mutations": results}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{sum(item['caught'] for item in results)}/{len(results)} injected faults detected")
    return 0 if all(item["caught"] for item in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
