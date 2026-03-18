"""Phase 2.2 test-gates: IR pair sensor."""

import pytest
from unittest.mock import MagicMock


@pytest.fixture
def ir_sensor():
    """IRPairSensor with controllable left/right mock pins."""
    import digitalio

    mock_left = MagicMock()
    mock_right = MagicMock()
    digitalio.DigitalInOut.side_effect = [mock_left, mock_right]

    from sensors.ir_pair import IRPairSensor
    sensor = IRPairSensor()

    digitalio.DigitalInOut.side_effect = None  # reset for subsequent tests
    return sensor


# ---------------------------------------------------------------------------
# read_position() for all 4 pin combinations
# ---------------------------------------------------------------------------

def test_read_position_line_left(ir_sensor):
    """Left on-line (value=False/0), right off-line (value=True/1) → -1.0."""
    ir_sensor._left.value = False
    ir_sensor._right.value = True
    assert ir_sensor.read_position() == -1.0


def test_read_position_line_right(ir_sensor):
    """Left off-line, right on-line → +1.0."""
    ir_sensor._left.value = True
    ir_sensor._right.value = False
    assert ir_sensor.read_position() == 1.0


def test_read_position_both_on_line(ir_sensor):
    """Both on-line → 0.0."""
    ir_sensor._left.value = False
    ir_sensor._right.value = False
    assert ir_sensor.read_position() == 0.0


def test_read_position_neither_on_line(ir_sensor):
    """Neither on-line → 0.0."""
    ir_sensor._left.value = True
    ir_sensor._right.value = True
    assert ir_sensor.read_position() == 0.0


# ---------------------------------------------------------------------------
# line_detected() for all 4 pin combinations
# ---------------------------------------------------------------------------

def test_line_detected_left_only(ir_sensor):
    ir_sensor._left.value = False
    ir_sensor._right.value = True
    assert ir_sensor.line_detected() is True


def test_line_detected_right_only(ir_sensor):
    ir_sensor._left.value = True
    ir_sensor._right.value = False
    assert ir_sensor.line_detected() is True


def test_line_detected_both(ir_sensor):
    ir_sensor._left.value = False
    ir_sensor._right.value = False
    assert ir_sensor.line_detected() is True


def test_line_detected_neither(ir_sensor):
    ir_sensor._left.value = True
    ir_sensor._right.value = True
    assert ir_sensor.line_detected() is False


# ---------------------------------------------------------------------------
# num_sensors and read_raw()
# ---------------------------------------------------------------------------

def test_num_sensors(ir_sensor):
    assert ir_sensor.num_sensors == 2


def test_read_raw_length(ir_sensor):
    ir_sensor._left.value = False
    ir_sensor._right.value = True
    assert len(ir_sensor.read_raw()) == 2


def test_read_raw_values_on_line(ir_sensor):
    """Left on-line → raw[0] == 0; right off-line → raw[1] == 1."""
    ir_sensor._left.value = False
    ir_sensor._right.value = True
    assert ir_sensor.read_raw() == [0, 1]


def test_read_raw_values_off_line(ir_sensor):
    """Both off-line → [1, 1]."""
    ir_sensor._left.value = True
    ir_sensor._right.value = True
    assert ir_sensor.read_raw() == [1, 1]
