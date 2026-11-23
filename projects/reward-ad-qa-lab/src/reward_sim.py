"""Deterministic fictional reward-ad flow for QA practice.

This is not a Buzzvil SDK or a model of any production reward service.
"""

from dataclasses import dataclass, field


@dataclass
class RewardFlow:
    initialized: bool = False
    consent: str = "UNKNOWN"
    online: bool = True
    state: str = "EMPTY"
    impressions: int = 0
    credited: set[str] = field(default_factory=set)
    credit_events: list[str] = field(default_factory=list)
    pending: set[str] = field(default_factory=set)
    events: list[dict] = field(default_factory=list)

    def snapshot(self) -> dict:
        return {
            "state": self.state,
            "impressions": self.impressions,
            "credited": sorted(self.credited),
            "credit_events": list(self.credit_events),
            "pending": sorted(self.pending),
        }

    def _record(self, action: str, accepted: bool, code: str, before: str, txn=None) -> dict:
        result = {"accepted": accepted, "code": code, "state": self.state}
        self.events.append({
            "seq": len(self.events) + 1, "action": action, "code": code,
            "from": before, "to": self.state, "txn": txn,
        })
        return result

    def command(self, action: str, value=None) -> dict:
        before = self.state
        if action == "initialize":
            if self.initialized:
                return self._record(action, False, "ALREADY_INITIALIZED", before)
            self.initialized = True
            return self._record(action, True, "INITIALIZED", before)

        if action == "set_consent":
            if value not in ("GRANTED", "DENIED"):
                return self._record(action, False, "INVALID_CONSENT", before)
            self.consent = value
            if value == "DENIED" and self.state == "LOADED":
                self.state = "EMPTY"
            return self._record(action, True, "CONSENT_UPDATED", before)

        if action == "disconnect":
            self.online = False
            return self._record(action, True, "OFFLINE", before)

        if action == "reconnect":
            self.online = True
            newly_credited = self.pending - self.credited
            self.credited.update(newly_credited)
            self.credit_events.extend(sorted(newly_credited))
            self.pending.clear()
            code = "PENDING_CREDITED" if newly_credited else "ONLINE"
            return self._record(action, True, code, before)

        if action == "load":
            if not self.initialized:
                return self._record(action, False, "NOT_INITIALIZED", before)
            if self.consent != "GRANTED":
                return self._record(action, False, "CONSENT_REQUIRED", before)
            if not self.online:
                return self._record(action, False, "NETWORK_UNAVAILABLE", before)
            if self.state != "EMPTY":
                return self._record(action, False, "INVALID_STATE", before)
            self.state = "LOADED"
            return self._record(action, True, "LOADED", before)

        if action == "show":
            if self.state != "LOADED":
                return self._record(action, False, "INVALID_STATE", before)
            if self.consent != "GRANTED":
                return self._record(action, False, "CONSENT_REQUIRED", before)
            self.state = "SHOWING"
            self.impressions += 1
            return self._record(action, True, "SHOWN", before)

        if action == "complete":
            if self.state != "SHOWING":
                return self._record(action, False, "INVALID_STATE", before, value)
            if not isinstance(value, str) or not value:
                return self._record(action, False, "INVALID_TXN", before, value)
            if value in self.credited or value in self.pending:
                return self._record(action, False, "DUPLICATE_IGNORED", before, value)
            if self.online:
                self.credited.add(value)
                self.credit_events.append(value)
                return self._record(action, True, "REWARD_CREDITED", before, value)
            self.pending.add(value)
            return self._record(action, True, "REWARD_PENDING", before, value)

        if action == "close":
            if self.state != "SHOWING":
                return self._record(action, False, "INVALID_STATE", before)
            self.state = "CLOSED"
            return self._record(action, True, "CLOSED", before)

        return self._record(action, False, "UNKNOWN_COMMAND", before)
