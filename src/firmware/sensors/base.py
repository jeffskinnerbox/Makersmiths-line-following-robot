class LineSensor:
    """Abstract base class for all line sensor modules."""

    @property
    def num_sensors(self):
        """Number of individual sensor elements."""
        raise NotImplementedError

    def calibrate(self):
        """Run calibration routine. Stores min/max values per sensor."""
        raise NotImplementedError

    def read_raw(self):
        """Return raw sensor readings as a list of integers.
        Length == num_sensors. 0 = on-line (dark), 1 = off-line (light)."""
        raise NotImplementedError

    def read_position(self):
        """Return estimated line position as a float.
        Range: -1.0 (line fully left) to +1.0 (line fully right). 0.0 = centered."""
        raise NotImplementedError

    def line_detected(self):
        """Return True if at least one sensor currently detects the line."""
        raise NotImplementedError
