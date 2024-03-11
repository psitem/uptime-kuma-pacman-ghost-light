# Pacman Ghost Light for Uptime Kuma

This is the [CircuitPython](https://circuitpython.org/) code used to build a [Paladone Pac-Man Ghost Light](https://amzn.to/49Cp8EF) whose lights adjust based on the status of monitors in [Uptime Kuma](https://uptime.kuma.pet/).

![Paladone Pacman Ghost Light](https://github.com/psitem/uptime-kuma-pacman-ghost-light/assets/5166927/01f93dea-0421-4b2c-8a7d-51fc4c953045)

##

#### Requirements: 
  - CircuitPython 8.x.
  - Compatibled board.
  - Adafruit NeoPixel-compatible RGB LEDs (ie: [WS2812b](https://amzn.to/43dU3Vh)).
  - [Uptime Kuma](https://uptime.kuma.pet/).

All necessary CircuitPython libraries are included in the `code/lib` directory.

Anything that runs CircuitPython and provides W-Fi, 5v, and 2 pins of GPIO ought to work (plus 3v3 and i2c if using the optional display). My development setup was on an [Raspberry Pi Pico W](https://www.raspberrypi.com/products/raspberry-pi-pico/?variant=raspberry-pi-pico-w) but deployed it with an [ESP-C3-13-Kit](https://amzn.to/3wOrRMG) board — that particular ESP board seems to be unobainium today but the [ESP-C3-12F-Kit](https://amzn.to/3PgFWsz) boards are probably equivalent.

#### Optional:
  - [SSD1306-compatible display](https://amzn.to/48IWCA0).

Note that the included `adafruit_displayio_ssd1306` library has been modified at line 57 to increase the scan rate.

#### Installation:

Copy everything from the `code/` directory to the CircuitPython root.

#### Configuration:

`settings.toml`:

* `METRICS_URL =` Complete URL to the Prometheus metrics endpoint on your Uptime Kuma instance (ie: http://something/metrics).
* `API_TOKEN =` Your Uptime Kuma API token. Needed if authentication is enabled. See `/settings/api-keys` on your Uptime Kuma instance.
* `CIRCUITPY_WIFI_SSID =` Wi-Fi SSID.
* `CIRCUITPY_WIFI_PASSWORD =` Wi-Fi password.
* `CIRCUITPY_WEB_API_PORT =` Set to use the CircuitPython Web Workflow (ie: if your board doesn't support the "CIRCUITPY" drive).
* `CIRCUITPY_WEB_API_PASSWORD =` Password for the CircuitPython Web Workflow (optional).

`code.py`:

Look for the part near the top that says Configuration Section.

General settings:
* `interval_refresh =` How often to check Uptime Kuma (in seconds).
* `interval_timeout =` How long to wait for Uptime Kuma response (in seconds).
* `use_ntp =` [ True | False ] Set the board clock using NTP.

Body LED settings:
* `use_body_pixels =` [ True | False ]
* `body_pixels_pin =` GPIO to use for body LEDs.
* `body_pixels_count =` Number of body LEDs.
* `body_pixels_brightness =` Body LED brightness, 1 = 100%.

Eye LED settings:
* `use_eye_pixels =` [ True | False ]
* `eye_pixels_pin =` GPIO to use for eye LEDs.
* `eye_pixels_count =` Number of eye LEDs.
* `eye_pixels_brightness =` Eye LED brightness, 1 = 100%.

LCD settings:
* `use_display =` [ True | False ]
* `scl_pin =` GPIO to use for i2c SCL
* `sda_pin =` GPIO to use for i2c SDA

#### Demo:

##### Pacman Ghost cycling through the light states:

https://github.com/psitem/uptime-kuma-pacman-ghost-light/assets/5166927/a5622c94-68ad-44a3-9a49-f24b3292df82

##### Test rig:
![Test setup with Pico W](https://github.com/psitem/uptime-kuma-pacman-ghost-light/assets/5166927/cf1119aa-5878-41fa-96da-d2a0e75dbe5c)
