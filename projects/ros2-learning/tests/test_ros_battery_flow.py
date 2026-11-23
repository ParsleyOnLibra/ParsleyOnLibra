import json
import sys
from pathlib import Path
from time import monotonic
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src" / "battery_qa"))

try:
    import rclpy
    from rclpy.executors import SingleThreadedExecutor
    from std_msgs.msg import String
    from battery_qa.battery_nodes import BatteryMonitorNode, BatteryPublisherNode
    HAS_ROS = True
except ImportError:
    HAS_ROS = False


@unittest.skipUnless(HAS_ROS, "ROS 2 rclpy is not installed in this environment")
class RosBatteryFlowTests(unittest.TestCase):
    def test_pub_sub_invalid_timeout_and_recovery(self):
        rclpy.init()
        executor = SingleThreadedExecutor()
        nodes = []
        try:
            publisher = BatteryPublisherNode(values=(19, 101, 20), period_seconds=0.08)
            monitor = BatteryMonitorNode(timeout_seconds=0.45, check_period_seconds=0.05)
            observer = rclpy.create_node("battery_qa_test_observer")
            nodes = [publisher, monitor, observer]
            observed = []
            observer.create_subscription(String, "/qa/battery_status",
                                         lambda message: observed.append(json.loads(message.data)), 10)
            for node in nodes:
                executor.add_node(node)

            deadline = monotonic() + 8.0
            while monotonic() < deadline:
                executor.spin_once(timeout_sec=0.05)
                statuses = {event["status"] for event in observed}
                if {"LOW", "INVALID", "NORMAL"}.issubset(statuses):
                    break
            self.assertTrue({"LOW", "INVALID", "NORMAL"}.issubset({e["status"] for e in observed}), observed)

            publisher.timer.cancel()
            deadline = monotonic() + 4.0
            while monotonic() < deadline and not any(e["status"] == "STALE" for e in observed):
                executor.spin_once(timeout_sec=0.05)
            self.assertTrue(any(e["status"] == "STALE" for e in observed), observed)

            before = len(observed)
            publisher.values = (20,)
            publisher.index = 0
            publisher.publish_next()
            deadline = monotonic() + 4.0
            while monotonic() < deadline and not any(e["status"] == "NORMAL" for e in observed[before:]):
                executor.spin_once(timeout_sec=0.05)
            self.assertTrue(any(e["status"] == "NORMAL" for e in observed[before:]), observed)
        finally:
            for node in nodes:
                executor.remove_node(node)
                node.destroy_node()
            executor.shutdown()
            rclpy.shutdown()


if __name__ == "__main__":
    unittest.main()
