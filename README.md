# Pacman Ghost Light for Uptime Kuma

This is the [CircuitPython](https://circuitpython.org/) code used to build a [Paladone Pac-Man Ghost Light](https://amzn.to/49Cp8EF) whose lights adjust based on the status of monitors in [Uptime Kuma](https://uptime.kuma.pet/).

![Paladone Pacman Ghost Light](https://github.com/psitem/uptime-kuma-pacman-ghost-light/assets/5166927/01f93dea-0421-4b2c-8a7d-51fc4c953045)

##### Demo of Pacman Ghost Light cycling through the light states:

https://github.com/psitem/uptime-kuma-pacman-ghost-light/assets/5166927/a5622c94-68ad-44a3-9a49-f24b3292df82

(My iPhone camera does not accurately capture the colors)

##

#### Requirements: 
  - [Uptime Kuma](https://uptime.kuma.pet/).
  - [CircuitPython](https://circuitpython.org/) 8.x.
  - [Compatible board with Wi-Fi](https://circuitpython.org/downloads?features=Wi-Fi).
  - Adafruit NeoPixel-compatible RGB LEDs (ie: [WS2812b](https://amzn.to/43dU3Vh)).

#### Optional:
  - [SSD1306-compatible 128x64 display](https://amzn.to/48IWCA0).

Any supported CircuitPython board that provides Wi-Fi, 5v, and 2 pins of GPIO ought to work (plus 3v3 and i2c if using a typical SSD1306 display). I've personally used this on a [Raspberry Pi Pico W](https://www.raspberrypi.com/products/raspberry-pi-pico/?variant=raspberry-pi-pico-w) and [ESP-C3-13-Kit](https://amzn.to/3wOrRMG). In my general experience, ESP32 boards have better Wi-Fi reliabilitiy than the Pico W. With CircuitPython on the Pico W the Wi-Fi library as of v8.2.10 does not change `wifi.radio.connected` to `False` when a Wi-Fi connection becomes unavailable until the radio or board is reset — on the ESP32-C3 it works as expected.

The specific ESP32-C3 board I've used does not seem to be available to purchase anywhere any more, but the [ESP-C3-12F-Kit](https://amzn.to/3PgFWsz) appears to be equivalent and of breadboard-friendly width.

#### Installation:

Copy everything from the `code/` directory to the CircuitPython root. All necessary CircuitPython libraries are included in the `code/lib` directory.

Note: The `adafruit_displayio_ssd1306` library has been modified at line 57 to increase the scan rate. Should that not work for your display, you can revert the modification or drop in the original from [Adafruit's CircuitPython Bundle](https://github.com/adafruit/Adafruit_CircuitPython_Bundle).

#### Configuration:

There are settings that MUST be configured for this to work.

* `settings.toml`:

  * `METRICS_URL =` Complete URL to the Prometheus metrics endpoint on your Uptime Kuma instance (ie: http://something/metrics). __Required.__
  * `API_TOKEN =` Your Uptime Kuma API token. Needed if authentication is enabled. See `/settings/api-keys` on your Uptime Kuma instance.
  * `CIRCUITPY_WIFI_SSID =` Wi-Fi SSID. __Required.__
  * `CIRCUITPY_WIFI_PASSWORD =` Wi-Fi password. __Required.__
  * `CIRCUITPY_WEB_API_PORT =` Set to use the CircuitPython Web Workflow (ie: if your board doesn't support the "CIRCUITPY" drive).
  * `CIRCUITPY_WEB_API_PASSWORD =` Password for the CircuitPython Web Workflow (optional).

* `settings.py`:
  * General settings:
    * `interval_refresh =` How often to check Uptime Kuma (in seconds).
    * `interval_timeout =` How long to wait for Uptime Kuma response (in seconds).
    * `use_ntp =` [ True | False ] Set the board clock using NTP.
  * Body LED settings:
    * `use_body_pixels =` [ True | False ]
    * `body_pixels_pin =` GPIO to use for body LEDs.
    * `body_pixels_count =` Number of body LEDs.
    * `body_pixels_brightness =` Body LED brightness, 1 = 100%.
  * Eye LED settings:
    * `use_eye_pixels =` [ True | False ]
    * `eye_pixels_pin =` GPIO to use for eye LEDs.
    * `eye_pixels_count =` Number of eye LEDs.
    * `eye_pixels_brightness =` Eye LED brightness, 1 = 100%.
  * LCD settings:
    * `use_display =` [ True | False ]
    * `scl_pin =` GPIO to use for i2c SCL
    * `sda_pin =` GPIO to use for i2c SDA

Some combination of Body LED, Eye LED, and LCD settings must be configured, or else it won't do anything beyond outputting to the serial port.

#### Modifying:

There are a series of functions prefixed with `action_` which control the LED states:

* `action_Booting:` Startup.
* `action_NoWifi:` Wi-Fi not yet connected.
* `action_HaveWifi:` Wi-Fi has connection.
* `action_Unreachable:` Uptime Kuma unreachable / non-responsive.
* `action_Pending:` Some Uptime Kuma monitors are in the Pending state.
* `action_Outage:` Some Uptime Kuma monitors are in the Outage state.
* `action_Up:` All Uptime Kuma monitors are Up.

For testing purposes, set `loop_light_states = True` in `settings.py` to infinitely loop through the color states.

#### Constructing:

Building and wiring up your Pacman Ghost is an exercise left up to you. Frankly, I barely know what I'm doing. 

The Pacman Ghost Light shell easily comes apart with four screws on the back and a bit of prying to release the tabs. Stripping out the guts is a couple more screws. My original proof-of-concept version used a [Pico W](https://www.raspberrypi.com/products/raspberry-pi-pico/?variant=raspberry-pi-pico-w), 5 RGB LEDs for the body, and recycled the white LEDs for the eyes (always on). My second incarnation runs an [ESP-C3-13-Kit](https://amzn.to/3wOrRMG), uses 9 RGB LEDs for the body, and adds two more RGB LEDs for the eyes. With the eyes I had to scrape the holes and surface a bit for a good-ish fit and hot glued the RGB LEDs in place.

![Pacman Ghost under construction](https://github.com/psitem/uptime-kuma-pacman-ghost-light/assets/5166927/0ee3dd5a-2fd9-4adf-ad54-b71aa3c7dfbf)

[A wiring diagram representative of my ESP32-C3 build](https://wokwi.com/projects/392092914913689601):

![ESP32-C3 Wiring Diagram](https://github.com/psitem/uptime-kuma-pacman-ghost-light/assets/5166927/8ada1c2f-d1fb-48da-a2e1-20f49ff6b936)

[A wiring diagram representative of my Pico W build](https://wokwi.com/projects/392090613383536641):

![Pico W Wiring Diagram](https://github.com/psitem/uptime-kuma-pacman-ghost-light/assets/5166927/d074d741-1e4a-47c7-974c-2534426ed473)

#### My test rig:

With a screen for debugging, two "eye" and three "body" LEDs.

![Test setup with Pico W](https://github.com/psitem/uptime-kuma-pacman-ghost-light/assets/5166927/cf1119aa-5878-41fa-96da-d2a0e75dbe5c)

(My iPhone camera does not accurately capture the LED colors)
