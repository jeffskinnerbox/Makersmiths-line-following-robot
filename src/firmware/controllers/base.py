class Controller:
    """Abstract base class for all control algorithm modules."""

    def update(self, position, dt):
        """Compute motor speeds from line position and time delta.
        Args:
            position: Line position from LineSensor.read_position() (-1.0 to +1.0)
            dt: Time elapsed since last update, in seconds
        Returns:
            (left_speed, right_speed): Motor speeds, each -1.0 to +1.0
        """
        raise NotImplementedError

    def reset(self):
        """Reset internal state (integral accumulator, etc.)."""
        raise NotImplementedError

    def get_params(self):
        """Return current tunable parameters as a dict."""
        raise NotImplementedError

    def set_params(self, params):
        """Update tunable parameters from a dict."""
        raise NotImplementedError

    @property
    def param_definitions(self):
        """Return metadata about tunable parameters for the browser UI."""
        raise NotImplementedError
