"""Phase 2.3 test-gates: bang-bang controller and integration."""

import pytest

from controllers.bang_bang import BangBangController
import config


@pytest.fixture
def controller():
    return BangBangController()


# ---------------------------------------------------------------------------
# update() outputs correct (left, right) for -1.0, 0.0, +1.0
# ---------------------------------------------------------------------------

def test_update_line_left(controller):
    """position < 0 → turn left: (turn_speed, base_speed)."""
    p = controller.get_params()
    left, right = controller.update(-1.0, 0.1)
    assert left == p['turn_speed']
    assert right == p['base_speed']


def test_update_line_right(controller):
    """position > 0 → turn right: (base_speed, turn_speed)."""
    p = controller.get_params()
    left, right = controller.update(1.0, 0.1)
    assert left == p['base_speed']
    assert right == p['turn_speed']


def test_update_centered(controller):
    """position == 0 → straight: (base_speed, base_speed)."""
    p = controller.get_params()
    left, right = controller.update(0.0, 0.1)
    assert left == p['base_speed']
    assert right == p['base_speed']


# ---------------------------------------------------------------------------
# set_params() takes effect in next update()
# ---------------------------------------------------------------------------

def test_set_params_base_speed_takes_effect(controller):
    controller.set_params({'base_speed': 0.5})
    left, right = controller.update(0.0, 0.1)
    assert left == 0.5
    assert right == 0.5


def test_set_params_turn_speed_takes_effect(controller):
    controller.set_params({'turn_speed': 0.1, 'base_speed': 0.4})
    left, right = controller.update(-1.0, 0.1)
    assert left == 0.1   # turn_speed
    assert right == 0.4  # base_speed


# ---------------------------------------------------------------------------
# get_params() / set_params() round-trip
# ---------------------------------------------------------------------------

def test_get_set_params_roundtrip(controller):
    original = controller.get_params()
    controller.set_params(original)
    assert controller.get_params() == original


def test_set_params_partial_preserves_other_keys(controller):
    """set_params with one key only updates that key."""
    original_turn = controller.get_params()['turn_speed']
    controller.set_params({'base_speed': 0.7})
    assert controller.get_params()['base_speed'] == 0.7
    assert controller.get_params()['turn_speed'] == original_turn


# ---------------------------------------------------------------------------
# reset() is a no-op and doesn't raise
# ---------------------------------------------------------------------------

def test_reset_no_error(controller):
    controller.reset()


# ---------------------------------------------------------------------------
# Integration: sensor → controller → motors via config
# ---------------------------------------------------------------------------

def test_integration_pipeline():
    """Full pipeline: config factories → position sequence → motor calls."""
    sensor = config.get_sensor()
    controller = config.get_controller()
    motors = config.get_motor_driver()

    for position in [-1.0, 0.0, 1.0, 0.0, -0.5, 0.5]:
        left, right = controller.update(position, 0.01)
        motors.set_speeds(left, right)

    motors.stop()
