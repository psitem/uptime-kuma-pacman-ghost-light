###
### You must configure some combination of pixels or display, else this won't do anything
### but output information to the serial port. Consult the README for more information on
### these settings and settings.toml
###

import os
import board

# URL for /metrics on your Uptime Kuma instance.
metrics_url = os.getenv("METRICS_URL")

# Need to provide an Uptime Kuma API token if authentication is enabled.
# See <Uptime Kuma URL>/settings/api-keys
api_token = os.getenv("API_TOKEN")

interval_refresh = 15
interval_timeout=30

# use_display = True              # Default False. Supports an SSD1306 i2c 128x64 display.
# scl_pin = board.GP15            # My Pico W setting
# sda_pin = board.GP14            # My Pico W setting

# use_ntp = True

# use_body_pixels = True          # Default False
# body_pixels_pin = board.GP27    # My Pico W setting
# body_pixels_count = 8
# body_pixels_brightness = 1  # Default 1 (100%).

# use_eye_pixels = True           # Default False
# eye_pixels_pin = board.GP28     # My Pico W setting
# eye_pixels_count = 2
# eye_pixels_brightness = 1   # Default 1 (100%).

# loop_light_states = False        # Default False. True will infinite loop through all the light states.
