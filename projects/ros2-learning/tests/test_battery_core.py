import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src" / "battery_qa"))
from battery_qa.battery_core import BatteryMonitorCore  # noqa: E402


class BatteryCoreTests(unittest.TestCase):
    def test_battery_boundary_and_range(self):
        monitor = BatteryMonitorCore(started_at=0.0)
        for level, status in ((0, "LOW"), (19, "LOW"), (20, "NORMAL"),
                              (21, "NORMAL"), (100, "NORMAL")):
            with self.subTest(level=level):
                event = monitor.ingest(level, now=1.0)
                self.assertTrue(event.accepted)
                self.assertEqual(event.status, status)
                self.assertEqual(event.level, level)

    def test_invalid_values_do_not_replace_last_valid(self):
        monitor = BatteryMonitorCore(started_at=0.0)
        monitor.ingest(50, now=1.0)
        for bad in (-1, 101, True, 20.0, None):
            with self.subTest(value=bad):
                event = monitor.ingest(bad, now=1.2)
                self.assertFalse(event.accepted)
                self.assertEqual(event.code, "INVALID_BATTERY")
                self.assertEqual(monitor.last_valid_level, 50)
                self.assertEqual(monitor.last_valid_at, 1.0)

    def test_missing_data_becomes_stale_once(self):
        monitor = BatteryMonitorCore(timeout_seconds=2.0, started_at=0.0)
        self.assertIsNone(monitor.check_timeout(1.99))
        self.assertEqual(monitor.check_timeout(2.0).status, "STALE")
        self.assertIsNone(monitor.check_timeout(3.0))

    def test_invalid_data_does_not_delay_timeout_and_valid_data_recovers(self):
        monitor = BatteryMonitorCore(timeout_seconds=2.0, started_at=0.0)
        monitor.ingest(19, now=1.0)
        monitor.ingest(101, now=2.9)
        self.assertEqual(monitor.check_timeout(3.0).status, "STALE")
        self.assertEqual(monitor.ingest(20, now=3.1).status, "NORMAL")
        self.assertIsNone(monitor.check_timeout(4.0))
        self.assertEqual(monitor.check_timeout(5.2).status, "STALE")


if __name__ == "__main__":
    unittest.main()
