import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "ros2-learning" / "src" / "battery_qa"))
sys.path.insert(0, str(ROOT / "amr-qa-lab" / "src"))
from battery_qa.amr_adapter import apply_to_robot  # noqa: E402
from battery_qa.battery_core import BatteryMonitorCore  # noqa: E402
from amr_sim import Robot  # noqa: E402


class AmrLinkTests(unittest.TestCase):
    def test_19_percent_blocks_and_20_percent_allows_mission(self):
        for level, code in ((19, "BATTERY_LOW"), (20, "MISSION_STARTED")):
            with self.subTest(level=level):
                robot = Robot()
                event = BatteryMonitorCore().ingest(level, now=1.0)
                self.assertEqual(apply_to_robot(robot, event)["code"], "BATTERY_SET")
                self.assertEqual(robot.command("start_mission")["code"], code)

    def test_invalid_battery_does_not_change_robot(self):
        robot = Robot(battery=50)
        event = BatteryMonitorCore().ingest(101, now=1.0)
        self.assertIsNone(apply_to_robot(robot, event))
        self.assertEqual(robot.battery, 50)


if __name__ == "__main__":
    unittest.main()
