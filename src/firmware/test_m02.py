# test_m02.py — M0.2 Hardware Verification
#
# Covers M0.2 test-gates:
#   Gate 1: CircuitPython version printed (visual confirm)
#   Gate 2: gc.mem_free() >= 100 KB reported
#   Gate 3: Both wheels spin via motor test
#
# SETUP:
#   1. Pico W must be seated in the Kitronik Robotics Board
#   2. 9V battery must be connected to the Kitronik board (motors won't spin without it)
#   3. Copy this file to CIRCUITPY/main.py
#   4. Open Mu Editor serial console — output appears on boot
#   5. After boot, call test_motors() in the REPL to re-run motor test
#
# No external libraries required — uses CircuitPython built-ins only.
"""
Development Workflow:
    # Edit code
    nvim test_m02.py

    # Copy to Pico W CircuitPython drive
    !cp % /media/jeff/CIRCUITPY/code.py

    # Monitor output
    tio /dev/ttyACM0
    enter `Ctrl-t q` to exit serial terminal `tio`
"""

import gc
import sys
import time
import board
import busio

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

KITRONIK_ADDR = 0x6C  # PCA9685 I2C address on Kitronik 5329 (default)

# Kitronik 5329 PCA9685 channel mapping (servos on CH0-7, motors on CH8-15)
# Motor 1 = left wheel, Motor 2 = right wheel (per spec §2.2 and §2.3)
# If a motor doesn't spin, swap FWD/REV for that motor, or try offset by ±2.
MOTOR1_FWD = 8
MOTOR1_REV = 9
MOTOR2_FWD = 10
MOTOR2_REV = 11


# ---------------------------------------------------------------------------
# PCA9685 low-level helpers (no external library)
# ---------------------------------------------------------------------------


def _pca_write(i2c, reg, data):
    """Write bytes to a PCA9685 register. i2c must be locked by caller."""
    i2c.writeto(KITRONIK_ADDR, bytes([reg]) + bytes(data))


def _pca_set_channel(i2c, channel, counts):
    """Set PCA9685 channel duty cycle. counts: 0-4095. 0 = fully off."""
    base = 0x06 + 4 * channel
    if counts <= 0:
        # FULL OFF: set OFF bit in LEDn_OFF_H
        _pca_write(i2c, base, [0x00, 0x00, 0x00, 0x10])
    else:
        counts = min(counts, 4095)
        _pca_write(i2c, base, [0x00, 0x00, counts & 0xFF, (counts >> 8) & 0x0F])


def _pca_wake(i2c):
    """Wake PCA9685 from sleep and enable register auto-increment."""
    # MODE1 = 0x20: AI=1 (auto-increment), SLEEP=0 (oscillator on)
    _pca_write(i2c, 0x00, [0x20])
    time.sleep(0.005)  # wait >= 500 us for oscillator to stabilize


# ---------------------------------------------------------------------------
# Test-gate functions
# ---------------------------------------------------------------------------


def check_system():
    """Gate 1 + Gate 2: print CP version and check free RAM >= 100 KB."""
    print("\n--- Gate 1 + 2: System Check ---")
    print(f"CircuitPython {sys.version}")
    free = gc.mem_free()
    kb = free // 1024
    ok = free >= 102400  # 100 KB
    print(
        f"Free RAM: {free} bytes ({kb} KB) [{'PASS' if ok else 'FAIL — expected >= 100 KB'}]"
    )
    return ok


def i2c_scan():
    """Scan I2C bus and confirm Kitronik board is present at 0x6C."""
    print("\n--- I2C Scan ---")
    try:
        i2c = busio.I2C(board.GP9, board.GP8)
    except RuntimeError as e:
        if "pull up" in str(e).lower():
            print("ERROR: No pull-ups on SDA/SCL.")
            print("  Most likely cause: Pico W not fully seated in Kitronik board.")
            print("  Fix: Remove and firmly re-seat Pico W, then reset.")
            print("  Fallback: add 4.7kΩ resistors GP8→3V3 and GP9→3V3 on breadboard.")
        else:
            print(f"I2C init error: {e}")
        return False
    while not i2c.try_lock():
        pass
    devices = i2c.scan()
    i2c.unlock()
    i2c.deinit()
    print(f"Devices found: {[hex(d) for d in devices]}")
    found = KITRONIK_ADDR in devices
    print(
        f"Kitronik board at {hex(KITRONIK_ADDR)}: {'FOUND' if found else 'NOT FOUND — check wiring'}"
    )
    return found


def test_motors(speed_pct=40, run_secs=1.5):
    """Gate 3: Spin each wheel individually, then both together.

    speed_pct : motor power 0-100 (40% is safe for bench test)
    run_secs  : how long each step runs
    """
    print(f"\n--- Gate 3: Motor Test ({speed_pct}% speed, {run_secs}s per step) ---")
    print("REMINDER: 9V battery must be connected to Kitronik board.")
    counts = int(speed_pct * 4095 / 100)

    try:
        i2c = busio.I2C(board.GP9, board.GP8)
    except RuntimeError as e:
        print(f"I2C init error: {e}")
        print("Re-seat Pico W in Kitronik board and reset.")
        return
    while not i2c.try_lock():
        pass

    try:
        _pca_wake(i2c)

        print("Step 1: Motor 1 FORWARD (left wheel) ...")
        _pca_set_channel(i2c, MOTOR1_FWD, counts)
        _pca_set_channel(i2c, MOTOR1_REV, 0)
        time.sleep(run_secs)
        _pca_set_channel(i2c, MOTOR1_FWD, 0)
        time.sleep(0.3)

        print("Step 2: Motor 2 FORWARD (right wheel) ...")
        _pca_set_channel(i2c, MOTOR2_FWD, counts)
        _pca_set_channel(i2c, MOTOR2_REV, 0)
        time.sleep(run_secs)
        _pca_set_channel(i2c, MOTOR2_FWD, 0)
        time.sleep(0.3)

        print("Step 3: Both motors FORWARD ...")
        _pca_set_channel(i2c, MOTOR1_FWD, counts)
        _pca_set_channel(i2c, MOTOR1_REV, 0)
        _pca_set_channel(i2c, MOTOR2_FWD, counts)
        _pca_set_channel(i2c, MOTOR2_REV, 0)
        time.sleep(run_secs)
        _pca_set_channel(i2c, MOTOR1_FWD, 0)
        _pca_set_channel(i2c, MOTOR2_FWD, 0)

        print("Motor test complete — did both wheels spin? If yes: PASS")
        print(
            "If a wheel didn't spin: try swapping MOTOR?_FWD/REV or shift channels by ±2"
        )

    except Exception as e:
        print(f"Motor test ERROR: {e}")

    finally:
        i2c.unlock()
        i2c.deinit()


# ---------------------------------------------------------------------------
# Auto-run on boot
# ---------------------------------------------------------------------------

mem_ok = check_system()
board_found = i2c_scan()

if mem_ok and board_found:
    print("\nGates 1-2: PASS")
    test_motors()
elif not board_found:
    print(
        "\nKitronik board not detected — check that Pico W is seated in board and wiring is correct."
    )
else:
    print("\nRAM check failed — unexpected for a fresh CircuitPython install.")

print("\nDone. Type test_motors() in REPL to re-run the motor test.")
