from controllers.base import Controller


class BangBangController(Controller):
    """Simple on/off steering controller for DS4–DS5.

    Turns left or right at full base_speed based on line position sign.
    No proportional scaling — just bang-bang switching.
    """

    def __init__(self):
        self._base_speed = 0.3
        self._turn_speed = 0.0

    def update(self, position, dt):
        """Return (left_speed, right_speed) based on line position.

        position < 0 → turn left:  (turn_speed, base_speed)
        position > 0 → turn right: (base_speed, turn_speed)
        position == 0 → straight:  (base_speed, base_speed)
        """
        if position < 0:
            return (self._turn_speed, self._base_speed)
        if position > 0:
            return (self._base_speed, self._turn_speed)
        return (self._base_speed, self._base_speed)

    def reset(self):
        pass  # no state to reset

    def get_params(self):
        return {'base_speed': self._base_speed, 'turn_speed': self._turn_speed}

    def set_params(self, params):
        if 'base_speed' in params:
            self._base_speed = params['base_speed']
        if 'turn_speed' in params:
            self._turn_speed = params['turn_speed']

    @property
    def param_definitions(self):
        return [
            {'name': 'base_speed', 'label': 'Base Speed',
             'min': 0.0, 'max': 1.0, 'step': 0.05, 'default': 0.3},
            {'name': 'turn_speed', 'label': 'Turn Speed',
             'min': 0.0, 'max': 1.0, 'step': 0.05, 'default': 0.0},
        ]
