"""Phase 3.1 test-gates: QTRX-MD-08RC sensor array (desktop, synthetic timing).

All GPIO interaction is bypassed by patching _read_raw_timings() with synthetic
discharge-time values. Tests cover DS6 gates 1-3 from the spec (§7.5).
"""

import pytest
from unittest.mock import patch

from sensors.qtrx_array import QTRXArray, _TIMEOUT_NS, _NUM_SENSORS


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def sensor():
    """QTRXArray with all GPIO mocked by conftest stubs."""
    return QTRXArray()


@pytest.fixture
def cal_sensor(sensor):
    """QTRXArray pre-calibrated: white=100 ns, black=800 ns per sensor."""
    sensor._cal_min = [100] * _NUM_SENSORS
    sensor._cal_max = [800] * _NUM_SENSORS
    return sensor


def _timings_for_sensor(active_idx, black_t=800, white_t=100):
    """Return timing list with one sensor set to black_t, rest white_t."""
    return [black_t if i == active_idx else white_t for i in range(_NUM_SENSORS)]


# ---------------------------------------------------------------------------
# Basic properties
# ---------------------------------------------------------------------------

def test_num_sensors(sensor):
    assert sensor.num_sensors == 8


# ---------------------------------------------------------------------------
# calibrate() — Gate 1: completes without error, stores correct bounds
# ---------------------------------------------------------------------------

def test_calibrate_no_error(sensor):
    """Gate 1: calibration completes without raising."""
    call_count = [0]

    def alt_timings():
        call_count[0] += 1
        return [800] * 8 if call_count[0] % 2 == 0 else [100] * 8

    with patch.object(sensor, '_read_raw_timings', side_effect=alt_timings):
        sensor.calibrate(samples=10)

    assert sensor._cal_min[0] == 100
    assert sensor._cal_max[0] == 800


def test_calibrate_tracks_per_sensor_min_max(sensor):
    """Each sensor's min/max tracked independently across samples."""
    # Timings vary by sample — different sensors see different ranges
    sample_data = [
        [200, 300, 400, 500, 500, 400, 300, 200],
        [100, 200, 300, 400, 600, 500, 400, 300],
        [150, 250, 350, 450, 550, 450, 350, 250],
    ]
    calls = [0]

    def fake_timings():
        result = sample_data[calls[0] % len(sample_data)]
        calls[0] += 1
        return result

    with patch.object(sensor, '_read_raw_timings', side_effect=fake_timings):
        sensor.calibrate(samples=3)

    assert sensor._cal_min[0] == 100  # min of [200, 100, 150]
    assert sensor._cal_max[0] == 200  # max of [200, 100, 150]
    assert sensor._cal_min[4] == 500  # min of [500, 600, 550]
    assert sensor._cal_max[4] == 600  # max of [500, 600, 550]


# ---------------------------------------------------------------------------
# read_raw() — Gate 2: distinct values, correct normalization
# ---------------------------------------------------------------------------

def test_read_raw_returns_eight_values(cal_sensor):
    with patch.object(cal_sensor, '_read_raw_timings', return_value=[450] * 8):
        raw = cal_sensor.read_raw()
    assert len(raw) == 8


def test_read_raw_all_white_is_zero(cal_sensor):
    """All sensors at cal_min → 0.0 (off-line)."""
    with patch.object(cal_sensor, '_read_raw_timings', return_value=[100] * 8):
        raw = cal_sensor.read_raw()
    assert all(v == 0.0 for v in raw)


def test_read_raw_all_black_is_one(cal_sensor):
    """All sensors at cal_max → 1.0 (on-line)."""
    with patch.object(cal_sensor, '_read_raw_timings', return_value=[800] * 8):
        raw = cal_sensor.read_raw()
    assert all(v == 1.0 for v in raw)


def test_read_raw_midpoint(cal_sensor):
    """Midpoint timing → ~0.5."""
    mid = (100 + 800) // 2  # 450
    with patch.object(cal_sensor, '_read_raw_timings', return_value=[mid] * 8):
        raw = cal_sensor.read_raw()
    for v in raw:
        assert abs(v - 0.5) < 0.01


def test_read_raw_black_greater_than_white(cal_sensor):
    """Gate 2: all 8 sensors report higher value on black than on white."""
    with patch.object(cal_sensor, '_read_raw_timings', return_value=[800] * 8):
        black_raw = cal_sensor.read_raw()
    with patch.object(cal_sensor, '_read_raw_timings', return_value=[100] * 8):
        white_raw = cal_sensor.read_raw()
    for b, w in zip(black_raw, white_raw):
        assert b > w


def test_read_raw_clamp_below_zero(cal_sensor):
    """Timing below cal_min clamps to 0.0."""
    with patch.object(cal_sensor, '_read_raw_timings', return_value=[50] * 8):
        raw = cal_sensor.read_raw()
    assert all(v == 0.0 for v in raw)


def test_read_raw_clamp_above_one(cal_sensor):
    """Timing above cal_max clamps to 1.0."""
    with patch.object(cal_sensor, '_read_raw_timings', return_value=[900] * 8):
        raw = cal_sensor.read_raw()
    assert all(v == 1.0 for v in raw)


def test_read_raw_zero_cal_span_no_divide_error(sensor):
    """Zero calibration span returns 0.0 without dividing by zero."""
    sensor._cal_min = [500] * 8
    sensor._cal_max = [500] * 8
    with patch.object(sensor, '_read_raw_timings', return_value=[500] * 8):
        raw = sensor.read_raw()
    assert all(v == 0.0 for v in raw)


# ---------------------------------------------------------------------------
# read_position() — Gate 3: line under extreme sensors -> ~±1.0
# ---------------------------------------------------------------------------

def test_read_position_line_under_sensor_1(cal_sensor):
    """Gate 3a: line under sensor 1 (index 0) -> ~-1.0."""
    with patch.object(cal_sensor, '_read_raw_timings',
                      return_value=_timings_for_sensor(0)):
        pos = cal_sensor.read_position()
    assert abs(pos - (-1.0)) < 0.05


def test_read_position_line_under_sensor_8(cal_sensor):
    """Gate 3b: line under sensor 8 (index 7) -> ~+1.0."""
    with patch.object(cal_sensor, '_read_raw_timings',
                      return_value=_timings_for_sensor(7)):
        pos = cal_sensor.read_position()
    assert abs(pos - 1.0) < 0.05


def test_read_position_line_centered(cal_sensor):
    """Line under sensors 4+5 (indices 3+4) -> ~0.0."""
    timings = [100] * 8
    timings[3] = 800
    timings[4] = 800
    with patch.object(cal_sensor, '_read_raw_timings', return_value=timings):
        pos = cal_sensor.read_position()
    assert abs(pos) < 0.15


def test_read_position_line_left_of_center(cal_sensor):
    """Line under sensor 3 (index 2) -> negative position."""
    with patch.object(cal_sensor, '_read_raw_timings',
                      return_value=_timings_for_sensor(2)):
        pos = cal_sensor.read_position()
    assert pos < 0.0


def test_read_position_line_right_of_center(cal_sensor):
    """Line under sensor 6 (index 5) -> positive position."""
    with patch.object(cal_sensor, '_read_raw_timings',
                      return_value=_timings_for_sensor(5)):
        pos = cal_sensor.read_position()
    assert pos > 0.0


def test_read_position_monotone_left_to_right(cal_sensor):
    """Position increases as line moves sensor 1 -> 8."""
    positions = []
    for idx in range(_NUM_SENSORS):
        with patch.object(cal_sensor, '_read_raw_timings',
                          return_value=_timings_for_sensor(idx)):
            positions.append(cal_sensor.read_position())
    for i in range(len(positions) - 1):
        assert positions[i] < positions[i + 1]


# ---------------------------------------------------------------------------
# Line-lost memory
# ---------------------------------------------------------------------------

def test_line_lost_returns_last_known_position(cal_sensor):
    """When line disappears, return the last known position."""
    with patch.object(cal_sensor, '_read_raw_timings',
                      return_value=_timings_for_sensor(7)):
        known = cal_sensor.read_position()

    with patch.object(cal_sensor, '_read_raw_timings', return_value=[100] * 8):
        lost_pos = cal_sensor.read_position()

    assert lost_pos == known


def test_line_lost_flag_set_when_no_line(cal_sensor):
    with patch.object(cal_sensor, '_read_raw_timings', return_value=[100] * 8):
        cal_sensor.read_position()
    assert cal_sensor.line_lost is True


def test_line_lost_flag_cleared_on_reacquire(cal_sensor):
    with patch.object(cal_sensor, '_read_raw_timings', return_value=[100] * 8):
        cal_sensor.read_position()
    with patch.object(cal_sensor, '_read_raw_timings',
                      return_value=_timings_for_sensor(3)):
        cal_sensor.read_position()
    assert cal_sensor.line_lost is False


def test_initial_position_is_zero(cal_sensor):
    """Default last_position is 0.0, returned on first lost-line read."""
    with patch.object(cal_sensor, '_read_raw_timings', return_value=[100] * 8):
        pos = cal_sensor.read_position()
    assert pos == 0.0


# ---------------------------------------------------------------------------
# line_detected()
# ---------------------------------------------------------------------------

def test_line_detected_true(cal_sensor):
    with patch.object(cal_sensor, '_read_raw_timings',
                      return_value=_timings_for_sensor(3)):
        assert cal_sensor.line_detected() is True


def test_line_detected_false(cal_sensor):
    with patch.object(cal_sensor, '_read_raw_timings', return_value=[100] * 8):
        assert cal_sensor.line_detected() is False
