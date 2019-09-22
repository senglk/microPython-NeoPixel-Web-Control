# microPython-NeoPixel-Web-Control

## Introduction

A micropython script where NeoPixel LED color cycles while webserver receives commands to turn on or off the LED.

This sample script starts a webserver which receives requests to turn on or off the NeoPixel LED. Upon receiving a `/?led=on` request, the NeoPixel LED will light up and color cycle. The NeoPixel LED will switch off upon receiving a `/?led=off` request.

The script is referenced from the tutorial [Raspberry Pi ESP32 MicroPython Tutorial](https://www.rototron.info/raspberry-pi-esp32-micropython-tutorial/), the tutorial [ESP32/ESP8266 MicroPython Web Server - Control Outputs](https://randomnerdtutorials.com/esp32-esp8266-micropython-web-server/), and asynchronous programming example [Demo of Simple uasyncio-Based Echo Server](https://github.com/peterhinch/micropython-async/blob/master/client_server/userver.py).

In particular, the 2 tutorials mentioned above does go into how to set up micropython on the ESP32 if this is your first time. I would recommend following at least 1 of the 2 tutorials above so that at least micropython is loaded onto the ESP32.

## Prerequisites

### MicroPython

This script was written for [MicroPython v1.11](http://docs.micropython.org/en/v1.11/).

### uasyncio

A library for [Asynchronous Programming in MicroPython](https://github.com/peterhinch/micropython-async).

You can install uasncio library in REPL with (the ESP32 needs to be connected to the internet):
````
>>> import upip
>>> upip.install('micropython-uasyncio')
````

This will install the uasyncio library in a `/pyboard/lib/uasyncio/` in the case of MicroPyton on ESP32.

For more information please refer to [installing uasyncio on bare metal](https://github.com/peterhinch/micropython-async/blob/master/TUTORIAL.md#01-installing-uasyncio-on-bare-metal) or [application of uasyncio to hardware interfaces](https://github.com/peterhinch/micropython-async/blob/master/TUTORIAL.md).

## Usage

### Updating the Pin Number

The pin number would also need to be changed to the pin number of the GPIO data pin connected to the data pin of the NeoPixel.

Currently the pin number follows the pin numbering in [Raspberry Pi ESP32 MicroPython Tutorial](https://www.rototron.info/raspberry-pi-esp32-micropython-tutorial/).

### Updating the WiFi SSID and Password

Please update with the SSID and Password in the line that calls `ap.config()`. This will be the SSID and password that will be used to connect to the ESP32. Currently this is set as `essid='yourSSID'` and `password='yourPassword'`, respectively.

### Uploading the Script

The script will then need to be uploaded into the ESP32. This can be done in many ways such as [uPyCraft IDE](https://randomnerdtutorials.com/install-upycraft-ide-windows-pc-instructions/) or [rshell](https://github.com/dhylands/rshell). If the file is uploaded as `main.py`, it will start automatically on reset.

### Starting the Script

You can start the script by soft resetting by pressing `Ctrl+D` on a blank line in REPL or by pressing `EN` on the ESP32 board.

### Controlling On and Off

After resetting the ESP32 board, connect to the Access Point broadcasted by the ESP32 based on the SSID and Password in the script, and connect to the IP address of the ESP32. This address should be `192.168.4.1`. For more information about ESP32 Access Point, see [this link](https://randomnerdtutorials.com/esp32-access-point-ap-web-server/). A webpage should pop up with On and Off buttons, which when pressed will switch the NeoPixel LED on or off, respectively. Note that the script starts the NeoPixel LED in an off state.

### Terminating the Script

You can terminate the script by pressing `Ctrl+C` in REPL, or by simply powering down the ESP32.
