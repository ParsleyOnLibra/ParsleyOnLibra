"""Deterministic AMR state machine used as a public QA practice target.

All thresholds and behaviors are fictional project requirements, not the
specification of any commercial robot.
"""

from dataclasses import dataclass, field


@dataclass
class Robot:
    map_loaded: bool = True
    route_valid: bool = True
    battery: int = 50
    dock_available: bool = True
    state: str = "IDLE"
    events: list[dict] = field(default_factory=list)

    def __post_init__(self):
        if type(self.battery) is not int or not 0 <= self.battery <= 100:
            raise ValueError("battery must be an integer from 0 to 100")

    def _record(self, action: str, accepted: bool, code: str, before: str) -> dict:
        result = {"accepted": accepted, "code": code, "state": self.state}
        self.events.append({"seq": len(self.events) + 1, "action": action,
                            "accepted": accepted, "code": code,
                            "from": before, "to": self.state})
        return result

    def command(self, action: str, value=None) -> dict:
        before = self.state
        if action == "set_battery":
            if type(value) is not int or not 0 <= value <= 100:
                return self._record(action, False, "INVALID_BATTERY", before)
            self.battery = value
            return self._record(action, True, "BATTERY_SET", before)

        if action == "press_estop":
            if self.state == "ESTOP":
                return self._record(action, False, "ALREADY_ESTOP", before)
            self.state = "ESTOP"
            return self._record(action, True, "ESTOP_PRESSED", before)

        if action == "release_estop":
            if self.state != "ESTOP":
                return self._record(action, False, "INVALID_STATE", before)
            self.state = "IDLE"  # A stopped mission never resumes automatically.
            return self._record(action, True, "ESTOP_RELEASED", before)

        if self.state == "ESTOP":
            return self._record(action, False, "ESTOP_ACTIVE", before)

        if action == "start_mission":
            if self.state != "IDLE":
                return self._record(action, False, "INVALID_STATE", before)
            if not self.map_loaded:
                return self._record(action, False, "MAP_MISSING", before)
            if not self.route_valid:
                return self._record(action, False, "ROUTE_INVALID", before)
            if self.battery < 20:
                return self._record(action, False, "BATTERY_LOW", before)
            self.state = "MOVING"
            return self._record(action, True, "MISSION_STARTED", before)

        if action == "detect_obstacle":
            if self.state != "MOVING":
                return self._record(action, False, "INVALID_STATE", before)
            self.state = "BLOCKED"
            return self._record(action, True, "OBSTACLE_DETECTED", before)

        if action == "clear_obstacle":
            if self.state != "BLOCKED":
                return self._record(action, False, "INVALID_STATE", before)
            self.state = "MOVING"
            return self._record(action, True, "OBSTACLE_CLEARED", before)

        if action == "request_dock":
            if self.state not in ("IDLE", "MOVING"):
                return self._record(action, False, "INVALID_STATE", before)
            if not self.dock_available:
                return self._record(action, False, "DOCK_UNAVAILABLE", before)
            self.state = "DOCKING"
            return self._record(action, True, "DOCKING_STARTED", before)

        if action == "dock_success":
            if self.state != "DOCKING":
                return self._record(action, False, "INVALID_STATE", before)
            self.state = "CHARGING"
            return self._record(action, True, "DOCKING_SUCCEEDED", before)

        if action == "dock_timeout":
            if self.state != "DOCKING":
                return self._record(action, False, "INVALID_STATE", before)
            self.state = "FAULT"
            return self._record(action, True, "DOCKING_TIMED_OUT", before)

        if action == "reset_fault":
            if self.state != "FAULT":
                return self._record(action, False, "INVALID_STATE", before)
            self.state = "IDLE"
            return self._record(action, True, "FAULT_RESET", before)

        return self._record(action, False, "UNKNOWN_COMMAND", before)
