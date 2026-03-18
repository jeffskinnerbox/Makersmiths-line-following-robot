"""Phase 2.1 test-gates: base classes, config factory functions, motor driver."""

import pytest

from sensors.base import LineSensor
from controllers.base import Controller
from motors.base import MotorDriver
from motors.kitronik import KitronikMotorDriver
import config


# ---------------------------------------------------------------------------
# Config factory functions return correct class types
# ---------------------------------------------------------------------------

def test_config_get_sensor_returns_linesensor():
    assert isinstance(config.get_sensor(), LineSensor)


def test_config_get_controller_returns_controller():
    assert isinstance(config.get_controller(), Controller)


def test_config_get_motor_driver_returns_motordriver():
    assert isinstance(config.get_motor_driver(), MotorDriver)


def test_config_get_speed_sensor_returns_none():
    assert config.get_speed_sensor() is None


def test_config_get_web_server_returns_none():
    assert config.get_web_server() is None


# ---------------------------------------------------------------------------
# set_speeds() and stop() accept valid inputs without raising
# ---------------------------------------------------------------------------

def test_set_speeds_forward():
    KitronikMotorDriver().set_speeds(0.5, 0.5)


def test_set_speeds_reverse():
    KitronikMotorDriver().set_speeds(-0.5, -0.5)


def test_set_speeds_mixed():
    KitronikMotorDriver().set_speeds(0.5, -0.5)


def test_stop():
    KitronikMotorDriver().stop()


# ---------------------------------------------------------------------------
# Deadband: |speed| < 0.05 → FULL OFF (zero duty cycle) on PCA9685
# ---------------------------------------------------------------------------

def test_set_speeds_deadband():
    import busio
    driver = KitronikMotorDriver()

    # Reset mock AFTER init so wake-call writes don't pollute the check
    mock_i2c = busio.I2C.return_value
    mock_i2c.writeto.reset_mock()

    driver.set_speeds(0.03, 0.03)

    assert mock_i2c.writeto.call_count == 4  # 4 channel writes (2 per motor)
    for c in mock_i2c.writeto.call_args_list:
        data = c[0][1]
        assert len(data) == 5, f"Expected 5-byte channel write, got {data.hex()}"
        assert data[4] == 0x10, f"Expected FULL OFF (0x10), got {data[4]:#04x}"


# ---------------------------------------------------------------------------
# set_speeds() clamps out-of-range values without raising
# ---------------------------------------------------------------------------

def test_set_speeds_clamp_high():
    KitronikMotorDriver().set_speeds(2.0, 1.5)


def test_set_speeds_clamp_low():
    KitronikMotorDriver().set_speeds(-2.0, -3.0)


# ---------------------------------------------------------------------------
# Main loop: config factories return usable objects (smoke-test without running loop)
# ---------------------------------------------------------------------------

def test_main_loop_instantiates_via_config():
    sensor = config.get_sensor()
    controller = config.get_controller()
    motors = config.get_motor_driver()
    assert isinstance(sensor, LineSensor)
    assert isinstance(controller, Controller)
    assert isinstance(motors, MotorDriver)
