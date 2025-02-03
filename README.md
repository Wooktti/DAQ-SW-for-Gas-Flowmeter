# Waterflow DAQ

## Introduction

S/W for DAQ system on injector water flow test. The S/W is designed to measure following sensor values.

- 2 Pressure Transducers (up to 70 barg @ max 100 Hz)
- 2 K-type thermocouples (up to 1024 degC @ max 4 Hz)
- 1 Flow Meter (up to 833 g/s @ max 100 Hz)

The newest version is designed for DAQ system utilizing Teensy 4.1 as its MCU.


This S/W is based on [Real-Time-Serial-Plotter](https://github.com/KAIST-THRUST/Real-Time-Serial-Plotter/tree/main) by THRUST.

## Installation

1. Clone or download this repository to your local machine.
2. Install PlatformIO extension via VSCode.
3. Install the required Python packages if they are not installed 
in your local computer.

```bash
pip install pyqtgraph pyserial pyQt5 numpy
```

## Hardware Setup

1. Make sure all of the sensors are connected to DAQ board. If you are not sure about the wiring, please contact to relavent PIC.
2. Remove the one side of jumper wires that are connected to channel A0, A1, and A2 of ADS1115 external ADC module.
3. Connect red and black aligator clip to 12VDC battery to power on the pressure transducers.
4. Connect the one side of jumper wires that are connected to channel A0, A1, and A2 of ADS1115.
5. Connect Teensy 4.1 and a laptop using a USB cable.
6. After the experiment, disconnect the jumper wire connected to A0, A1, and A2 of ADS1115, then remove 12VDC battery.

