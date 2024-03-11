import os
import board
import busio
import gc
import io
import re
import rtc
import socketpool
import supervisor
import sys
import time
import wifi
import adafruit_requests
import neopixel
import bitbangio

from base64 import b64encode
from settings import *

# The RegEx where the magic happens.
reobj=re.compile('^(?:monitor_status{.*}\s)(\d)')

# Colors
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
ORANGE = (255, 128, 0)
WHITE = (255,255,255)
OFF = (0,0,0)

body_pixels = None
eye_pixels = None

if ( not 'loop_light_states' in globals() ):
    loop_light_states = False
if ( not 'body_pixels_count' in globals() ):
    body_pixels_count = 1
if ( not 'body_pixels_brightness' in globals() ):
    body_pixels_brightness = 0
if ( not 'body_pixels_count' in globals() ):
    body_pixels_count = 0
if ( not 'use_body_pixels' in globals() ):
    use_body_pixels = False
    body_pixels = None
if ( use_body_pixels ):
    if ( not 'body_pixels_brightness' in globals() ):
        body_pixels_brightness = 0.025
    body_pixels = neopixel.NeoPixel(body_pixels_pin, body_pixels_count, brightness=body_pixels_brightness, auto_write=True)
    body_pixels.fill(OFF)

if ( not 'eye_pixels_count' in globals() ):
    eye_pixels_count = 2
if ( not 'eye_pixels_brightness' in globals() ):
    eye_pixels_brightness = 0
if ( not 'eye_pixels_count' in globals() ):
    eye_pixels_count = 0
if ( not 'use_pixels' in globals() ):
    eye_use_pixels = False
    eye_pixels = None
if ( use_eye_pixels ):
    if ( not 'eye_pixels_brightness' in globals() ):
        eye_pixels_brightness = 0.025
    eye_pixels = neopixel.NeoPixel(eye_pixels_pin, eye_pixels_count, brightness=eye_pixels_brightness,auto_write=True)
    eye_pixels.fill(OFF)


if ( not 'use_display' in globals() ):
    use_display = False

if ( not 'interval_refresh' in globals() ):
    interval_refresh = 15

if ( not 'metrics_url' in globals() ):
    metrics_url = None

if ( ('api_token' in globals()) ):
    auth_credentials = ":" + api_token
    auth_token = b64encode(auth_credentials.encode("utf-8")).decode("ascii")
    headers = {'Authorization': 'Basic ' + auth_token}
else:
    headers = {'Authorization': 'None'}

if ( not 'use_ntp' in globals() ):
    use_ntp = False
if ( use_ntp ):
    import adafruit_ntp

def action_Booting():
    if ( use_eye_pixels ):
        eye_pixels.fill(RED)
    elif ( use_body_pixels ):
        body_pixels.fill(WHITE)
    time.sleep(2)
    pass

def action_NoWifi():
    if ( use_eye_pixels ):
        eye_pixels.fill(RED)
    elif ( use_body_pixels ):
        body_pixels.fill(BLUE)
    time.sleep(2)

def action_HaveWifi():
    if ( (use_eye_pixels) and (use_body_pixels) ):
        eye_pixels.fill(WHITE)
        body_pixels.fill(WHITE)
    elif ( use_eye_pixels ):
        eye_pixels.fill(WHITE)
    elif (use_body_pixels):
        body_pixels.fill(PURPLE)
    time.sleep(2)
    pass

def action_Unreachable():
    if ( (use_eye_pixels) and (use_body_pixels) ):
        eye_pixels.fill(ORANGE)
    if ( use_body_pixels ):
        body_pixels.fill(ORANGE)
    time.sleep(2)

def action_Pending():
    if ( use_eye_pixels ):
        eye_pixels.fill(WHITE)
    if ( use_body_pixels ):
        body_pixels.fill(YELLOW)
    time.sleep(2)

def action_Outage():
    if ( use_eye_pixels ):
        eye_pixels.fill(WHITE)
    if ( use_body_pixels ):
        body_pixels.fill(RED)
    time.sleep(2)

def action_Up():
    if ( use_eye_pixels ):
        eye_pixels.fill(WHITE)
    if ( use_body_pixels ):
        body_pixels.fill(GREEN)
    time.sleep(2)

if ( use_display ):
    # This is what I do to set up a 128x64 SSD1306 OLED i2c display to show five lines
    # of terminal output. It's all very dirty but the point is to have a display for
    # debugging purposes.
    
    # If you have some other display, set it up here.

    import displayio
    import adafruit_displayio_ssd1306
    displayio.release_displays()

    i2c = busio.I2C(scl_pin, sda_pin)
    #i2c = bitbangio.I2C(scl_pin, sda_pin)
    display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
    display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64)
    display.root_group[0].hidden = False

    try:
        display.root_group.remove(display.root_group[2])
        display.root_group.remove(display.root_group[1])
    except Exception as e:
        e = None

    # I don't understand what's going on here, I took this from a GitHub issue. The height SHOULD be 64. 
    # Probably I should just find a font of the correct dimensions but 🤷‍♂️ #yolo
    supervisor.reset_terminal(display.width, 84)

    # My OLED is yellow/blue, the offset here gets the top pixels of the 2nd row out of the yellow.
    display.root_group[0].y = 2
    display.root_group[0].x = 0

# Loop through light actions.
while ( loop_light_states ):
    print ("action_Booting()")
    action_Booting()

    print("action_NoWifi()")
    action_NoWifi()

    print("action_HaveWifi()")
    action_HaveWifi()

    print("action_Unreachable()")
    action_Unreachable()

    print("action_Pending()")
    action_Pending()

    print("action_Outage()")
    action_Outage()

    print("action_Up()")
    action_Up()

    time.sleep(3)
    if ( use_body_pixels ):
        body_pixels.fill(OFF)
    if ( use_eye_pixels ):
        eye_pixels.fill(OFF)
    time.sleep(3)

action_Booting()

while ( True ):
    ssid = os.getenv("CIRCUITPY_WIFI_SSID")
    password = os.getenv("CIRCUITPY_WIFI_PASSWORD")

    radio = wifi.radio
    pool = socketpool.SocketPool(radio)

    wifiloopcount = 0
    while ( (not wifi.radio.ipv4_address) or (not wifi.radio.connected )  ):
        wifiloopcount += 1
        if ( wifiloopcount > 24 ):
            supervisor.reload()

        action_NoWifi()

        try:
            print("Connecting to AP...")
            print("wifi.radio.connected: " + str(wifi.radio.connected))
            print("wifi.radio.ipv4_address: " + str(wifi.radio.ipv4_address))
            print("wifiloopcount: " + str(wifiloopcount))
            wifi.radio.connect(ssid, password)
            if ( wifiloopcount > 1 ):
                time.sleep(5)
        except ConnectionError as e:
            print("could not connect to AP, retrying: ", e)
            e = None                

    action_HaveWifi()

    if ( use_ntp ):
        ntp = adafruit_ntp.NTP(pool, tz_offset=0)
        timeset = False
        loopcount = 0
        while ( (not timeset) and (loopcount < 5) ):
            try:
                loopcount += 1
                rtc.RTC().datetime = ntp.datetime
                timeset = True
            except Exception as e:
                time.sleep(10)
    
    loopcount = 0
    while ( True ):
        loopcount += 1
        if ( loopcount > 5 ):
            supervisor.reload()

        if ( loopcount > 2 ):
            action_Unreachable()

        dt = rtc.RTC().datetime
        seconds=dt.tm_sec
        minutes=dt.tm_min
        hour=dt.tm_hour
        dt = None

        wifiloopcount = 0
        while ( (not wifi.radio.ipv4_address) or (not wifi.radio.connected ) ):
            wifiloopcount += 1
            if ( wifiloopcount > 5 ):
                supervisor.reload()
            action_NoWifi()
            try:
                if ( wifiloopcount > 1 ):
                    time.sleep(5)
                print("Connecting to AP...")
                print("wifi.radio.connected: " + str(wifi.radio.connected))
                print("wifi.radio.ipv4_address: " + str(wifi.radio.ipv4_address))
                print("wifiloopcount: " + str(wifiloopcount))
                wifi.radio.connect(ssid, password)
            except ConnectionError as e:
                print("could not connect to AP, retrying: ", e)
                e = None                
                
        try:
            downcount = 0
            upcount = 0
            pendingcount = 0
            maintenancecount = 0 
            requests = adafruit_requests.Session(pool, None)

            response = requests.get(metrics_url, headers=headers, timeout=interval_timeout)
            respcode = response.status_code
            if ( respcode != 200 ):
                print("Time:       " + f'{hour:02d} {minutes:02d} {seconds:02d}')
                print("Status: " + f'{respcode:>12}')
                print("Loopcount: " + f'{loopcount:>9}')
                print("Memory free: " + f'{gc.mem_free():>7}')
                response.close()

                if ( loopcount > 1 ):
                    action_Unreachable()

            else:
                resptxt = response.text
                response.close()

                for line in io.StringIO(resptxt):
                    ## HELP monitor_status Monitor Status (1 = UP, 0= DOWN, 2= PENDING, 3= MAINTENANCE)
                    ## monitor_status{monitor_name="name",monitor_type="http",monitor_url="http://mynameisurl",monitor_hostname="null",monitor_port="null"} 1
                    res = reobj.match(line)
                    if ( res ):
                        if ( res.group(1) == '0' ):
                            downcount += 1
                        elif ( res.group(1) == '1' ):
                            upcount += 1
                        elif ( res.group(1) == '2' ):
                            pendingcount += 1
                        elif ( res.group(1) == '3' ):
                            maintenancecount += 1
                        else:
                            # print(res.group(1))
                            pass

                print("")
                print("Loopcount: " + f'{loopcount:>9}')
                print("Memory free: " + f'{gc.mem_free():>7}')
                
                print(f'{hour:02d} {minutes:02d} {seconds:02d}' + "           " + str(loopcount))
                print("Up: " + str(upcount))
                print("Down: " + str(downcount))
                print("Pending: " + str(pendingcount))
                print("Maintenance: " + str(maintenancecount))

                loopcount = 0

                if ( downcount > 0 ):
                    action_Outage()
                elif ( pendingcount > 0 ):
                    action_Pending()
                else:
                    action_Up()
       
        except Exception as e:
            print(f'{hour:02d} {minutes:02d} {seconds:02d}' + "   " + str(loopcount)  + " " + f'{gc.mem_free():>7}')
            print(e)
            e = None

            try: 
                response.close()
            except Exception as ex:
                ex = None

            action_Unreachable()

            response = None
            requests = None

        resptxt = None
        response = None
        requests = None
        dt = None
        downcount = None
        upcount = None
        pendingcount = None
        maintenancecount = None 

        gc.collect()
        time.sleep(interval_refresh)
        