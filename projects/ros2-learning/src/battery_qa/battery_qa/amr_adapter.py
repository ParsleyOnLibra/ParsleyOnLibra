"""Apply a validated battery event to the separate fictional AMR simulator."""

from .battery_core import BatteryEvent


def apply_to_robot(robot, event: BatteryEvent) -> dict | None:
    if not event.accepted or event.level is None:
        return None
    return robot.command("set_battery", event.level)
