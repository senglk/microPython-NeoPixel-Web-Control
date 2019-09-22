"""
NeoPixel Color Cycle and On Off Webserver Example
Created by combining:
Color cycle: https://www.rototron.info/raspberry-pi-esp32-micropython-tutorial/
Webserver: https://randomnerdtutorials.com/esp32-esp8266-micropython-web-server/
uasyncio: https://github.com/peterhinch/micropython-async/blob/master/client_server/userver.py
"""

from machine import Pin
from neopixel import NeoPixel
import usocket as socket
import uasyncio as asyncio
import uselect as select
import gc
import network

html = '<html><head><title>ESP Web Server</title>\
<meta name="viewport" content="width=device-width, initial-scale=1">\
<link rel="icon" href="data:,"><style>{}</style>\
</head><body><h1>ESP Web Server</h1><p>State: {}</p>\
<p><a href="/?led=on"><button class="button">ON</button></p>\
<p><a href="/?led=off"><button class="button button2">OFF</button></p></body></html>'

css = 'html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}\
h1{color: #0F3376; padding: 2vh;}p{font-size: 1.5rem;}.button{display: inline-block; background-color: #e7bd3b; border: none;\
border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}\
.button2{background-color: #4286f4;}'

def hsv_to_rgb(h, s, v):
    """
    Convert HSV to RGB (based on colorsys.py).

        Args:
            h (float): Hue 0 to 1.
            s (float): Saturation 0 to 1.
            v (float): Value 0 to 1 (Brightness).
    """
    
    if s == 0.0:
        return v, v, v
    i = int(h * 6.0)
    f = (h * 6.0) - i
    p = v * (1.0 - s)
    q = v * (1.0 - s * f)
    t = v * (1.0 - s * (1.0 - f))
    i = i % 6

    q = v * (1.0 - s * f)
    t = v * (1.0 - s * (1.0 - f))
    i = i % 6

    v = int(v * 255)
    t = int(t * 255)
    p = int(p * 255)
    q = int(q * 255)

    if i == 0:
        return v, t, p
    if i == 1:
        return q, v, p
    if i == 2:
        return p, v, t
    if i == 3:
        return p, q, v
    if i == 4:
        return t, p, v
    if i == 5:
        return v, p, q

def setNeoPixel(neopixel, r, g, b):
    neopixel[0] = (r, g, b)
    neopixel.write()

async def sendWebPage(conn, np_state):
    response = html.format(css, np_state,)
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    conn.close()

async def changeNeoPixelColor(spectrum, np):
    while True:
        for c in spectrum:
            hue = c / 2048.0
            r, g, b = hsv_to_rgb(hue, 1, .15)
            setNeoPixel(np, r, g, b)
            await asyncio.sleep_ms(10)

async def run(s_sock, loop, spectrum, np, np_state):
    coroColorChange = changeNeoPixelColor(spectrum, np)
    poller = select.poll()
    poller.register(s_sock, select.POLLIN)
    while True:
        res = poller.poll(1)  # 1ms block
        if res:  # Only s_sock is polled
            conn, addr = s_sock.accept()  # get client socket
            request = conn.recv(1024)
            request = str(request)
            led_on = request.find('/?led=on')
            led_off = request.find('/?led=off')
            if led_on == 6 and np_state == "OFF":
                np_state = "ON"
                loop.create_task(coroColorChange)
            if led_off == 6 and np_state == "ON":
                np_state = "OFF"
                asyncio.cancel(coroColorChange)
                setNeoPixel(np, 0, 0, 0)
                coroColorChange = changeNeoPixelColor(spectrum, np)
            # Implies if led_on and "ON", dont change state
            # Implies if led_off and "OFF", dont change state
            loop.create_task(sendWebPage(conn, np_state))
        await asyncio.sleep_ms(200)

"""
Neopixel data is connected to Pin 13
Replace 13 with the pin number your set up is using
"""
np = NeoPixel(Pin(13), 1)

"""
Turn off Neopixel on boot
"""
setNeoPixel(np, 0, 0, 0)
np_state = "OFF"

"""
Generate a list of colors the NeoPixel will cycle into
"""
spectrum = list(range(2048)) + list(reversed(range(2048)))

"""
Start Access Point
The ESP32 module will create it's own wireless access point for a devices to connect to
Replace the SSID and password of the access point below
authmode = 3 starts service with WPA2-PSK
"""
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid='yourSSID', authmode=3, password='yourPassword')

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

loop = asyncio.get_event_loop()

try:
    loop.run_until_complete(run(s, loop, spectrum, np, np_state))
except KeyboardInterrupt:
    print('Interrupted')
finally:
    setNeoPixel(np, 0, 0, 0)
    for sock in [s]:
        sock.close()
    ap.active(False)
    gc.collect()
