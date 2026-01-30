# Complete Digispark ATtiny85 Setup(macOS)
This guide is a complete guide to setting up the Digispark ATtiny85 board on macOS with the Arduino Uno as ISP and Arduino IDE.

## Prerequisites
- [Digispark ATtiny85](https://www.kickstarter.com/projects/digistump/digispark-the-tiny-arduino-enabled-usb-dev-board)
- [Arduino IDE](https://www.arduino.cc/en/software)
- [Arduino Uno](https://store.arduino.cc/products/arduino-uno-rev3)
- [avrdude](https://github.com/avrdudes/avrdude)
- [Micronucleus](https://github.com/micronucleus/micronucleus/releases)
- USB-A to USB-B Cable
- Breadboard
- Jumper Wires
- 10uF Capacitor

**Before you begin:** Have your Arduino Uno, Digispark ATtiny85, USB cable, 10 µF capacitor, jumper wires, and breadboard ready. First-time setup typically takes about 30–45 minutes.

## Steps
1. [Install Arduino IDE](#1-install-arduino-ide)
2. [Turn Arduino Uno into ISP](#2-turn-arduino-uno-into-isp)
3. [Install avrdude](#3-install-avrdude)
4. [Connect Digispark ATtiny85 to Arduino Uno](#4-connect-digispark-attiny85-to-arduino-uno)
5. [Use avrdude CLI to burn bootloader to Digispark ATtiny85 with Arduino Uno as ISP](#5-use-avrdude-cli-to-burn-bootloader-to-digispark-attiny85-with-arduino-uno-as-isp)
6. [Install Digispark AVR Boards in Arduino IDE](#6-install-digispark-avr-boards-in-arduino-ide)
7. [Verify Environment with Sample 'Blinking LED' Script](#7-verify-environment-with-sample-blinking-led-script)
8. [Upload and Execute Script](#8-upload-and-execute-script)


### 1. Install Arduino IDE

- Downloading the `.app`: https://www.arduino.cc/en/software
- Using Homebrew

```bash
$ brew install --cask arduino-ide
```

### 2. Turn Arduino Uno into ISP
Connect your Arduino Uno via USB. In Arduino IDE, go to **File** → **Examples** → **11. ArduinoISP** → **ArduinoISP** to open the ArduinoISP sketch. Click the Upload (arrow) button to upload it to your Uno. The Arduino Uno can now act as an ISP for the Digispark ATtiny85.

When you are ready to wire the Digispark (Step 4) and burn the bootloader (Step 5), keep the Uno connected to USB so it can power the Digispark and communicate with avrdude.


### 3. Install avrdude

```bash
$ brew install avrdude
```

### 4. Connect Digispark ATtiny85 to Arduino Uno
First, examine the pinout of ATtiny85 according to the [datasheet](https://ww1.microchip.com/downloads/en/devicedoc/atmel-2586-avr-8-bit-microcontroller-ATtiny25-ATtiny45-ATtiny85_datasheet.pdf).

![ATtiny25/45/85 Pinout](./images/pinout-attiny.png)

For the Digispark ATtiny85, the pin out matches the Port B pins of the ATtiny85.

![Digispark ATtiny85 Pinout](./images/pinout-digispark.png)

Connect the Digispark ATtiny85 to the Arduino Uno as follows:

| Digispark ATtiny85 Pin | ATtiny85 PhysicalPin | Arduino GPIO/Pin | Function |
|:------------------:|:----------------:|:--------:|:--------:|
| VIN | 8 | 5v | 5V |
| GND | 4 | GND | GND |
| 0 | 5 | 11 | MOSI |
| 1 | 6 | 12 | MISO |
| 2 | 7 | 13 | SCK |
| 5 | 1 | 10 | RESET |

For example, connect Digispark ATtiny85 pin 0 to Arduino Uno pin 11, Digispark ATtiny85 pin 1 to Arduino Uno pin 12, etc.

Also connect a 10 µF capacitor between Arduino **RST** and **GND**. If using an electrolytic capacitor, put the anode on RST and cathode on GND. A ceramic 10 µF capacitor has no polarity—either lead can go to RST or GND.

The Digispark is powered by the Uno’s 5V via the VIN–5V connection; the Uno must be connected to USB during the bootloader burn in Step 5.

### 5. Use avrdude CLI to burn bootloader to Digispark ATtiny85 with Arduino Uno as ISP

**Order of operations:** Upload ArduinoISP to the Uno (Step 2) → Wire the Digispark to the Uno (Step 4) with the 10 µF capacitor → Connect the Uno to your Mac via USB → Run avrdude below.

In Arduino IDE, go to **Tools** → **Port** and note the port your Arduino Uno is using (e.g. **/dev/cu.usbmodemXXXX** on macOS). If you unplug and replug the Uno, the port may change—re-check if avrdude fails to open the device.

In a terminal, find the avrdude config file location:

```bash
$ which avrdude
```

- If avrdude is at **/usr/local/bin/avrdude** (Intel Mac), the config is **avrdude.conf** in **/usr/local/Cellar/avrdude/&lt;version&gt;/.bottle/etc/**
- If at **/opt/homebrew/bin/avrdude** (Apple Silicon), look in **/opt/homebrew/Cellar/avrdude/&lt;version&gt;/.bottle/etc/**

Download the [t85_default.hex](https://github.com/micronucleus/micronucleus/blob/master/firmware/releases/t85_default.hex) file (Micronucleus bootloader) from the micronucleus repo. Place it in the directory where you will run avrdude, or use its full path in the command.

**Fuse warning:** The commands below set fuse bytes (lfuse, hfuse, efuse). Do not change these values unless you know what they do; wrong values can lock the chip or prevent it from running.

Set the environment variables and run the following to burn the bootloader:
```bash
$ export AVRDUDE_PORT=<your_arduino_port>
$ export AVRDUDE_CONF=<path_to_avrdude_config_file>
$ avrdude -C $AVRDUDE_CONF \
  -v -p t85 -c stk500v1 -P $AVRDUDE_PORT -b 19200 \
  -U flash:w:t85_default.hex:i \
  -U lfuse:w:0xe1:m -U hfuse:w:0xdd:m -U efuse:w:0xfe:m
```

Example:

```bash
$ export AVRDUDE_PORT=/dev/cu.usbmodem14201
$ export AVRDUDE_CONF=/usr/local/Cellar/avrdude/8.0/.bottle/etc/avrdude.conf

$ avrdude -C $AVRDUDE_CONF \
  -v -p t85 -c stk500v1 -P $AVRDUDE_PORT -b 19200 \
  -U flash:w:t85_default.hex:i \
  -U lfuse:w:0xe1:m -U hfuse:w:0xdd:m -U efuse:w:0xfe:m
Avrdude version 8.0
Copyright see https://github.com/avrdudes/avrdude/blob/main/AUTHORS

System wide configuration file is /usr/local/Cellar/avrdude/8.0/.bottle/etc/avrdude.conf
User configuration file /Users/taiy/.avrduderc does not exist

Using port            : /dev/cu.usbmodem14101
Using programmer      : stk500v1
Setting baud rate     : 19200
AVR part              : ATtiny85
Programming modes     : SPM, ISP, HVSP, debugWIRE
Programmer type       : STK500
Description           : Atmel STK500 v1
HW Version            : 2
FW Version            : 1.18
Topcard               : Unknown
Vtarget               : 0.0 V
Varef                 : 0.0 V
Oscillator            : Off
SCK period            : 0.0 us
XTAL frequency        : 7.372800 MHz

AVR device initialized and ready to accept instructions
Device signature = 1E 93 0B (ATtiny85)
Auto-erasing chip as flash memory needs programming (-U flash:w:...)
specify the -D option to disable this feature
Erased chip

Processing -U flash:w:t85_default.hex:i
Reading 1514 bytes for flash from input file t85_default.hex
in 1 section [0x1a00, 0x1fe9]: 24 pages and 22 pad bytes
Writing 1514 bytes to flash
Writing | ################################################## | 100% 2.21 s 
Reading | ################################################## | 100% 1.10 s 
1514 bytes of flash verified

Processing -U lfuse:w:0xe1:m
Reading 1 byte for lfuse from input file 0xe1
in 1 section [0, 0]
Writing 1 byte (0xE1) to lfuse, 1 byte written, 1 verified

Processing -U hfuse:w:0xdd:m
Reading 1 byte for hfuse from input file 0xdd
in 1 section [0, 0]
Writing 1 byte (0xDD) to hfuse, 1 byte written, 1 verified

Processing -U efuse:w:0xfe:m
Reading 1 byte for efuse from input file 0xfe
in 1 section [0, 0]
Writing 1 byte (0xFE) to efuse, 1 byte written, 1 verified

Avrdude done.  Thank you.
```

Now the bootloader should be burned to the Digispark ATtiny85.

### 6. Install Digispark AVR Boards in Arduino IDE
1) Update board source

**digistump.com** has been down for a while, so we need to use the **github** mirror for the board manager.

In Arduino IDE, go to **File** -> **Preferences** and dump the following into the **Additional Boards Manager URLs** box:

[https://raw.githubusercontent.com/digistump/arduino-boards-index/master/package_digistump_index.json](https://raw.githubusercontent.com/digistump/arduino-boards-index/master/package_digistump_index.json)

If that URL does not work (e.g. 404), you can run a local server that serves the board index. From this repo’s directory:

```bash
$ pip install fastapi uvicorn
$ uvicorn app:app --reload
```

Then in **Additional Boards Manager URLs** use:

```
http://127.0.0.1:8000/package_digistump_index.json
```

Arduino IDE should then fetch the board index from your local server. Example server output:

```bash
$ uvicorn app:app --reload
INFO:     Will watch for changes in these directories: ['/Users/taiy/Documents/GitHub/digispark-attiny85-setup']
INFO:     Uvicorn running on http://192.168.2.196:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [49490] using StatReload
INFO:     Started server process [49513]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     192.168.2.250:49902 - "GET / HTTP/1.1" 404 Not Found
INFO:     192.168.2.250:49904 - "GET /package_digistump_index.json HTTP/1.1" 200 OK
INFO:     192.168.2.250:49544 - "GET /package_digistump_index.json HTTP/1.1" 200 OK
INFO:     192.168.2.250:49581 - "HEAD /package_digistump_index.json HTTP/1.1" 405 Method Not Allowed
INFO:     192.168.2.250:49581 - "GET /package_digistump_index.json HTTP/1.1" 200 OK
INFO:     192.168.2.250:49585 - "HEAD /package_digistump_index.json HTTP/1.1" 405 Method Not Allowed
INFO:     192.168.2.250:49585 - "GET /package_digistump_index.json HTTP/1.1" 200 OK
```

2) Install the Digistump AVR Boards  
In Arduino IDE, go to **Tools** → **Board** → **Boards Manager**. In the **Type** dropdown, select **Contributed** (Arduino IDE 2.x may show **All** or another label—look for **Digistump AVR Boards**). Select **Digistump AVR Boards** and click **Install**.

3) Set the default board  
Go to **Tools** → **Board** → **Digistump AVR Boards** → **Digispark (Default - 16.5mhz)**.

### 7. Verify Environment with Sample 'Blinking LED' Script
1) Paste the following blinking LED script into the sketch present in Arduino IDE:

```sketch
void setup() {
    pinMode(1, OUTPUT);
}

void loop() {
    digitalWrite(1, HIGH);
    delay(1000);
    digitalWrite(1, LOW);
    delay(2000);
}
```

2) Verify the script before you upload it, by clicking "Verify" in the top-left corner (alternately, **Sketch** -> **Verify/compile**).

If all is well, you should see the following output in the console at the bottom:
```
Sketch uses 2700 bytes (44%) of program storage space. Maximum is 6012 bytes.
Global variables use 95 bytes of dynamic memory.
```

**NB**: However, if you experience the following error: 
```
fork/exec /Users/XXXXX/Library/Arduino15/packages/arduino/tools/avr-gcc/4.8.1-arduino5/bin/avr-g++: bad CPU type in executable
Error compiling for board Digispark (Default - 16.5mhz).
```

The solution is to substitute (link) the built-in, outdated AVR tools that Digistump config looks for, with the new, updated one included in the Arduino IDE (Thanks to user [Anjin from the Digistump boards](https://digistump.com/board/index.php/topic,3198.msg14379.html#msg14379)). It is done in the following way:

For Arduino IDE 1.x:
```bash
$ cd ~/Library/Arduino15/packages/arduino/tools/avr-gcc
$ mv 4.8.1-arduino5 orig.4.8.1
$ ln -s /Applications/Arduino.app/Contents/Java/hardware/tools/avr 4.8.1-arduino5
```

For Arduino IDE 2.x (thanks to [@jorgezazo](https://gist.github.com/dbdness/072b032ecbab80578730345dbe68fb5b?permalink_comment_id=4730896#gistcomment-4730896) and [vgenov-py](https://gist.github.com/dbdness/072b032ecbab80578730345dbe68fb5b?permalink_comment_id=4787674#gistcomment-4787674)):

```bash
$ cd ~/Library/Arduino15/packages/arduino/tools/avr-gcc 
$ mv 4.8.1-arduino5/ orig.4.8.1 
$ ln -s ~/Library/Arduino15/packages/arduino/tools/avr-gcc/7.3.0-atmel3.6.1-arduino7 4.8.1-arduino5
```

### 8. Upload and Execute Script
Once the sketch verifies successfully, get the Digispark ATtiny85 board but **do not plug it in yet**.

1. In Arduino IDE, select **Tools** → **Board** → **Digistump AVR Boards** → **Digispark (Default - 16.5mhz)**.
2. In **Tools** → **Programmer**, select **Micronucleus**. This is required so the bootloader is not overwritten; otherwise you would need to burn the bootloader again.
3. Click **Upload** in the top left and wait for the prompt: 

```
Running Digispark Uploader...
Plug in device now... (will timeout in 60 seconds)
```

4. Plug in the Digispark via USB and wait. The following should appear in the Arduino console and the sketch should start running on the board:

```bash
> Device is found!
connecting: 16% complete
connecting: 22% complete
connecting: 28% complete
connecting: 33% complete
> Device has firmware version 1.6
> Available space for user applications: 6012 bytes
> Suggested sleep time between sending pages: 8ms
> Whole page count: 94  page size: 64
> Erase function sleep duration: 752ms
parsing: 50% complete
> Erasing the memory ...
erasing: 55% complete
erasing: 60% complete
erasing: 65% complete
> Starting to upload ...
writing: 70% complete
writing: 75% complete
writing: 80% complete
> Starting the user app ...
running: 100% complete
>> Micronucleus done. Thank you!
```

---

## Troubleshooting

| Issue | What to try |
|-------|-------------|
| **avrdude: ser_open(): can't open device** | Wrong or changed port. In Arduino IDE, **Tools** → **Port** and note the correct `/dev/cu.usbmodemXXXX`. Unplug/replug the Uno and re-check. Set `AVRDUDE_PORT` to that value. |
| **Device signature = 0x000000** or **initialization failed** | Wiring or power: confirm all six connections (VIN→5V, GND→GND, 0→11, 1→12, 2→13, 5→10) and the 10 µF capacitor (RST–GND). Ensure the Uno is connected to USB so it powers the Digispark. |
| **bad CPU type in executable** (avr-g++) | You are on Apple Silicon (M1/M2/M3). Apply the AVR tool symlink fix in Step 7 (Arduino IDE 2.x) so the Digistump toolchain uses a compatible compiler. |
| **Plug in device now... (will timeout in 60 seconds)** then timeout | Try a different USB port, a USB 2.0 hub, or a different USB cable. Some Macs and USB 3 ports do not enumerate the Digispark reliably. |
| **404** when adding board URL | Use the local server fallback in Step 6: run `uvicorn app:app --reload` from this repo and use `http://127.0.0.1:8000/package_digistump_index.json`. |