#ifndef DAQ_SETTING_H
#define DAQ_SETTING_H

#include <Arduino.h>
#include <ADS1X15.h>
#include <MAX6675.h>

// Modify the constants here.
/*********************************************************************/
#define SERIAL_BAUDRATE 115200 // serial communication baud rate

#define PT1_ADC_CH 0  // ADS1115 ADC channel that corresponds to pressure transducer 1
#define PT2_ADC_CH 1  // ADS1115 ADC channel that corresponds to pressure transducer 2
#define FM_ADC_CH 2  // ADS1115 ADC channel that corresponds to flow meter

#define TT1_CS 36 // MAX6675 Thermocouple 1 chip select
#define TT2_CS 37 // MAX6675 Thermocouple 2 chip select

#define ADS1115_ADDR 0x48 // ADS1115 I2C address, default is 0x48.
#define R_MAGNITUDE 150 // ohm, shunt resistor resistance

#define SENSOR_RATE 10     // sensor rate, in milliseconds
/*********************************************************************/

void print_value_to_serial(unsigned long time);

extern ADS1115 ADS; // Pressure Transducer 4-20mA -> shunt resistor -> ADC // Thermocouple analog reading -> ADC
extern MAX6675 tc1;
extern MAX6675 tc2;

#endif
