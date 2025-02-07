#ifndef DAQ_SETTING_H
#define DAQ_SETTING_H

#include <Arduino.h>
#include <ADS1X15.h>

// Modify the constants here.
/*********************************************************************/
#define SERIAL_BAUDRATE 115200 // serial communication baud rate

#define FM_ADC_CH 0  // ADS1115 ADC channel that corresponds to flow meter

#define ADS1115_ADDR 0x48 // ADS1115 I2C address, default is 0x48.
#define R_MAGNITUDE 150 // ohm, shunt resistor resistance

#define SENSOR_RATE 10     // sensor rate, in milliseconds

// #define MONITOR_METHOD 0 // 0: Send collected string data so that you can directly read sensor values from a serial monitor.
#define MONITOR_METHOD 1 // 1: Send raw binary data so that you can read them by 'water_flow_daq_realTimePlot.py' app.
/*********************************************************************/

void print_value_to_serial(unsigned long time);

extern ADS1115 ADS; // Pressure Transducer 4-20mA -> shunt resistor -> ADC // Thermocouple analog reading -> ADC

#endif
