"""Deterministic battery validation and timeout rules without ROS imports."""

from dataclasses import dataclass


@dataclass(frozen=True)
class BatteryEvent:
    status: str
    accepted: bool
    level: int | None
    code: str

    def as_dict(self) -> dict:
        return {"status": self.status, "accepted": self.accepted,
                "level": self.level, "code": self.code}


class BatteryMonitorCore:
    def __init__(self, timeout_seconds: float = 2.0, started_at: float = 0.0):
        if timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be positive")
        self.timeout_seconds = timeout_seconds
        self.started_at = started_at
        self.last_valid_at: float | None = None
        self.last_valid_level: int | None = None
        self.status = "UNKNOWN"

    def ingest(self, level: object, now: float) -> BatteryEvent:
        if type(level) is not int or not 0 <= level <= 100:
            self.status = "INVALID"
            return BatteryEvent("INVALID", False, None, "INVALID_BATTERY")
        self.last_valid_level = level
        self.last_valid_at = now
        self.status = "LOW" if level < 20 else "NORMAL"
        return BatteryEvent(self.status, True, level, "BATTERY_ACCEPTED")

    def check_timeout(self, now: float) -> BatteryEvent | None:
        reference = self.last_valid_at if self.last_valid_at is not None else self.started_at
        if now - reference < self.timeout_seconds or self.status == "STALE":
            return None
        self.status = "STALE"
        return BatteryEvent("STALE", False, self.last_valid_level, "BATTERY_TIMEOUT")
