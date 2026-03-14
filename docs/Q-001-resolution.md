
Gemini Prompt:
_What pins on the  Robotics Board for Raspberry Pi Pico - <https://www.pishop.us/product/robotics-board-for-raspberry-pi-pico/>
are consumed by the board and cannot be used for general purposes? Give me the reference document you found this information._


The Robotics Board for Raspberry Pi Pico (Kitronik Product Code 5329) consumes the following pins for its onboard operations,
which are not recommended for general-purpose use:

GP8 and GP9 (I2C Bus): These pins are used for the I2C communication protocol to control the onboard 16-channel PWM driver IC
and the two Dual H-Bridge motor driver ICs.
While these pins are broken out to a header to allow you to add other I2C-compatible devices,
they cannot be used for general-purpose digital I/O without interfering with the board's motor and servo control.

3V3 (Pin 36) and GND: The board uses these pins to provide a regulated 3.3V supply directly to the
Raspberry Pi Pico from its own onboard voltage regulator.
This allows the entire setup to be powered from a single battery or power source (3V to 10.8V) connected to the board,
removing the need to power the Pico separately via USB.

According to the official documentation, all other pins on the Raspberry Pi Pico are "unused" by the board's internal circuitry
and are broken out for general-purpose use, including sensors, LEDs, or other inputs.
The board features 27 I/O expansion points (including the 26 standard GPIO/ADC pins and the RUN pin) that remain available for your projects.

Reference Document
The information above is found in the Kitronik Compact Robotics Board for Raspberry Pi Pico Datasheet (Product Code 5329).

Official Product Page: [Kitronik 5329 Product Page](https://kitronik.co.uk/products/5329-kitronik-compact-robotics-board-for-raspberry-pi-pico)
Datasheet PDF: [Kitronik 5329 Datasheet](https://download.kamami.pl/p1193902-5329-Pico-robotics-board-datasheet.pdf)
