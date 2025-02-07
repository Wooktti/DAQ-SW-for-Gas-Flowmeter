# DAQ for Gas flowmeter

## Introduction

S/W for DAQ system on the gas flow meter (TMF series). The S/W is designed to measure following sensor values.

- 1 TMF Series Gas Flow Meter (up to 200slm, 4-20mA output)

The newest version is designed for DAQ system utilizing Teensy 4.1 as its MCU.

This S/W is modified for the usage of a gas flow meter reading, and based on [waterflow_daq](https://github.com/KAIST-THRUST/waterflow_daq) by THRUST.

## Installation

1. Clone or download this repository to your local machine.
2. Install PlatformIO extension via VSCode.
3. Install the required Python packages if they are not installed 
in your local computer.

```bash
pip install pyqtgraph pyserial pyQt5 numpy
```

## Hardware Setup

1. Wire 4-20mA current signal line from the flowmeter to the DAQ circuit. The corresponding ADC channel on ADS1115 is Channel 0.
2. Connect 24VDC power to the flowmeter.
3. Connect Teensy 4.1 and a laptop using a USB cable.

