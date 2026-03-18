class MotorDriver:
    """Abstract base class for motor driver modules."""

    def set_speeds(self, left, right):
        """Set motor speeds. Range: -1.0 (full reverse) to +1.0 (full forward)."""
        raise NotImplementedError

    def stop(self):
        """Immediately stop both motors (set speed to 0, not coast)."""
        raise NotImplementedError
