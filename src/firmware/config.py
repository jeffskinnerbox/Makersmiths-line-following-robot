# DS3–DS5 firmware configuration
# Change SENSOR / CONTROLLER / MOTOR_DRIVER constants when swapping modules for a new DS.

SENSOR = "ir_pair"
CONTROLLER = "bang_bang"
MOTOR_DRIVER = "kitronik"
SPEED_SENSOR = None
WIFI_ENABLED = False

BASE_SPEED = 0.3
TURN_SPEED = 0.0


def get_sensor():
    """Return configured LineSensor instance."""
    from sensors.ir_pair import IRPairSensor
    return IRPairSensor()


def get_controller():
    """Return configured Controller instance with current speed params."""
    from controllers.bang_bang import BangBangController
    c = BangBangController()
    c.set_params({'base_speed': BASE_SPEED, 'turn_speed': TURN_SPEED})
    return c


def get_motor_driver():
    """Return configured MotorDriver instance."""
    from motors.kitronik import KitronikMotorDriver
    return KitronikMotorDriver()


def get_speed_sensor():
    """Return speed sensor instance, or None if not configured."""
    return None  # not used until DS9


def get_web_server():
    """Return web server instance, or None if WiFi disabled."""
    return None  # not used until DS8
