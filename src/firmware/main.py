"""main.py — LFR cooperative polling loop.

Runs on the Pico W. Auto-executed by CircuitPython on boot.
Not covered by desktop pytest — smoke-test manually via Mu Editor serial console.
"""

import gc
import time

import config


def main():
    sensor = config.get_sensor()
    controller = config.get_controller()
    motors = config.get_motor_driver()
    web_server = config.get_web_server()

    sensor.calibrate()

    last_time = time.monotonic()

    while True:
        now = time.monotonic()
        dt = now - last_time
        last_time = now

        position = sensor.read_position()
        left_speed, right_speed = controller.update(position, dt)
        motors.set_speeds(left_speed, right_speed)

        if web_server:
            web_server.poll()

        gc.collect()


main()
