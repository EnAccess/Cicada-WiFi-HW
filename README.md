# Cicada-WiFi-HW


Cicada WiFi HW - IoT Communications Module for Energy Access.
An easy way to get production ready, bi-directional communications for your IoT embedded device.

This repository contains the hardware design for supported Cicada wifi.


Manufacturing files:
If you are only interested in manufacturing the PCBs, you only need files in the /manufacturing/ directory.
send them to your contract manufacturer of choice, Some examples of turnkey PCBA manufacturers are:
-Seed Studios
-JLCPCB
-PCBCart
-Bittele
The /manufacturing/production directory contains the PCB Gerber/drill files, the BOM, and assembly instructions.


Source files:
If you'd like to take a look at the schematics and PCB layout, first, make sure you have a fresh version of KiCAD. It's a free and open source electronics design tool, 
and can be downloaded from http://kicad.org. Make sure you are not using an old version that some Linux distributions might be still shipping.


File structure:
The schematics and related files live under the /design/ directory:

/design/doc/datasheets/ - Datasheets for some of the components used. Obviously, not covered by the LICENSE. 
/design/pdfs/ - Schematics exported as PDF. 
/design/renders - 3D renders of the PCBs. 
/design/source/ltspice - Ltspice simulations, mainly concerning power usage and decoupling capacitors. 
/design/source/kicad - The juicy bits.


The latest manufacturing files live under the /manufacturing/ directory
/manufacturing/production - PCB output files(gerber files,POS files,dril files and stackup setiles), BOM, Assembly instruction,etc.


A quick look at the schematics:
The schematics is based on ESP-07S ESP8266 Serial WiFi Module, The module supports standard IEEE802.11 b/g/n agreement, complete TCP/IP protocol stack and capable of 
+20dBm output power in 802.11b mode. For more information the data sheet of the module will be available in /design/doc/datasheets/ directory


Host interface:
The Cicada uses a 2x10 female pin socket that fits perfectly in a 2x8 shrouded pin header on the host side. (We don’t use a 2x8 female pin socket because it is possible to 
do a off-by-one insertion with it). The host interface provides a way for the host to detect the presence of a Cicada board,transmit and receive data, and distinguish 
between different Cicada communications boards (Cicada 2g, Cicada 4g):

Pin-5	  5V              power
Pin-1	  Vref(3v3)       logic level VCC reference.
Pin-2	  VER_1           Board version pin (represents, what type of cicada it is 2g,4g or WiFi)
Pin-3	  VER_2           Board version pin (represents, latest production release version)
Pin-12	UART_Tx_3V3
Pin-13	UART_Rx_3V3
Pin-8	  POWER enable    drive high to enable power.
Pin-16	RESET pin       drive low to reset, drive at 1.8 - 3.3v during normal operation. 


Power:
Board is powered up by single-chip SMPS (HX3406) to convert 5v down to 3.3v required by ESP-07S(ESP8266 Serial WiFi Module WiFi module).



Antenna:
The ESP-07S ESP8266 Serial WiFi Module has a on board IPEX connector, which can be extended to an antenna using U.FL cable 



HW Modes:
MODE      GPIO15      GPIO0     GPIO2

UART      low         low       high
FLASH     low         high      high


Need to Flash the module with the latest FW??

Requirements:
-USB to serial TTL adapter hardware
-esptool.py (Ubuntu package esptool or GitHub - espressif/esptool: Espressif SoC serial bootloader utility)
-Wifi firmware: https://www.espressif.com/sites/default/files/ap/ESP8266_NonOS_AT_Bin_V1.7.4.zip
Note: Make sure the USB to serial adapter is set to 3.3V IO voltage! (usually there is a jumper for that)


Setup:
Connect Wifi module and USB adapter

Cicada WiFi       USB adapter
  5V0              	   5V0
  GND                  GND
  POWER_EN             3V3
  UART_RX_3V3          Tx
  UART_TX_3V3          Rx
Note: that RX/TX are cross connected
The module should now respond to AT commands. You can check this by running the serial_linux example from Cicada.


Flash firmware:
Connect IO0 (Pin 12) and GND (Pin 9) directly on the ESP-07s chip. This sets the chip into UART firmware programming mode.

Unzip the firmware package and go to ESP8266_NonOS_AT_Bin_V1.7.4/bin directory. Then run this command to flash:
esptool.py -p /dev/ttyUSB0 --chip esp8266 write_flash --flash_size 4MB-c1 0x00000 boot_v1.7.bin 0x01000 at/1024+1024/user1.2048.new.5.bin 0x1fc000 esp_init_data_default_v08.bin 0xfe000 blank.bin 0x1fb000 blank.bin 0x1fe000 blank.bin

After flashing, remove the grounding of IO0 again, so it’s free floating. The Cicada module should now be ready for installation.


Future Improvements:



