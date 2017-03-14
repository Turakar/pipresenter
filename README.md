# PiPresenter

<img alt="PiPresenter Logo" src="https://raw.githubusercontent.com/Turakar/pipresenter/master/material/logo.png" width="600">

## Overview
The PiPresenter is a mod for your Pi which adds the ability to easily show presentations from your USB-stick or your Moodle account.
The UI is displayed on a touchscreen by a python program.
This project is aimed for schools, but might be used in other areas like universities or companies, too.
The PiPresenter is a project for "Jugend Forscht", a german science competition.

## Features
- easy to use and simple presentation tool
- display files from your stick directly without an additional laptop
- or download your file from a Moodle server
- intuitive and simple UI
- way cheaper than a laptop
- more reliable than a laptop

## Description

### Hardware
- Raspberry Pi (tested with version 3)
- Touchscreen (currently only [Kuman 3.5" resistive touchscreen from Amazon](https://www.amazon.de/Kuman-Resolution-Display-Protective-Raspberry/dp/B01FX7909Q))
- SD-Card
- Micro USB power source
- HDMI cable or adapter
- USB keyboard

### Software
The software is based on Raspbian Lite.
The main program is written in python and uses PyGame to display an interface on the touchscreen.
The python program also manages the X Server and the presentation program (e.g. LibreOffice).
The program is splitted into the three parts pipresenter.py (controlling and drawing the UI), hardware.py (interaction with the OS and other programs) and moodle.py (Moodle client).

## Installation
Have a look at the [installation instructions](INSTALL.md).
I will probably make this installation easier in the future by providing a custom image.

## Known Problem with the touchscreen
The touchscreen from Kuman turns white after the pi shuts down. I already designed a circuit featuring a Teensy (I had this one laying around, you could use any microcontroller you want) with an MOSFET to turn the power off after not receiving a signal from the Pi for a longer time. But this one is not done yet.
