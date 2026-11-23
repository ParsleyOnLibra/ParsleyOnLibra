"""ROS 2 publisher and monitor for a fictional integer battery percentage."""

import json
from time import monotonic

import rclpy
from rclpy.node import Node
from std_msgs.msg import Int16, String

from .battery_core import BatteryMonitorCore, BatteryEvent


BATTERY_TOPIC = "/qa/battery_pct"
STATUS_TOPIC = "/qa/battery_status"


class BatteryPublisherNode(Node):
    def __init__(self, values=(21, 20, 19, -1, 101, 50), period_seconds=1.0):
        super().__init__("battery_qa_publisher")
        self.values = tuple(values)
        if not self.values:
            raise ValueError("values must not be empty")
        self.index = 0
        self.publisher = self.create_publisher(Int16, BATTERY_TOPIC, 10)
        self.timer = self.create_timer(period_seconds, self.publish_next)

    def publish_next(self):
        value = self.values[self.index % len(self.values)]
        self.index += 1
        message = Int16()
        message.data = value
        self.publisher.publish(message)
        self.get_logger().info(f"battery_pct={value}")


class BatteryMonitorNode(Node):
    def __init__(self, timeout_seconds=2.0, check_period_seconds=0.1):
        super().__init__("battery_qa_monitor")
        self.core = BatteryMonitorCore(timeout_seconds, monotonic())
        self.publisher = self.create_publisher(String, STATUS_TOPIC, 10)
        self.subscription = self.create_subscription(Int16, BATTERY_TOPIC, self.on_battery, 10)
        self.timer = self.create_timer(check_period_seconds, self.on_watchdog)

    def emit(self, event: BatteryEvent):
        message = String()
        message.data = json.dumps(event.as_dict(), ensure_ascii=False)
        self.publisher.publish(message)
        self.get_logger().info(message.data)

    def on_battery(self, message: Int16):
        self.emit(self.core.ingest(message.data, monotonic()))

    def on_watchdog(self):
        event = self.core.check_timeout(monotonic())
        if event is not None:
            self.emit(event)


def publisher_main(args=None):
    rclpy.init(args=args)
    node = BatteryPublisherNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


def monitor_main(args=None):
    rclpy.init(args=args)
    node = BatteryMonitorNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()
