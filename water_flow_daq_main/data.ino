#include "daq_setting.h"

float get_pressure(float voltage) {
  // Convert voltage to current (in mA)
  float current = voltage / R_MAGNITUDE * 1000.0; // mA
  return ((current - 4.0) * 68.9476 / 16.0); // bar
}

// 4~20mA = 0~833g/s
float get_flow(float voltage) {
  // Convert voltage to current (in mA)
  float current = voltage / R_MAGNITUDE * 1000.0;
  return ((current - 4.0) * 833.0 / 16.0); // g/s
}

void print_value_to_serial(unsigned long time) {
  float press1_bar, press2_bar, temp_1_degC, temp_2_degC, FM_g_per_s;
  int16_t pt1_raw_volt, pt2_raw_volt, fm_raw_volt;

  pt1_raw_volt = ADS.readADC(PT1_ADC_CH); // pressure 1 raw value reading from ADS1115
  pt2_raw_volt = ADS.readADC(PT2_ADC_CH); // pressure 2 raw value reading from ADS1115
  fm_raw_volt = ADS.readADC(FM_ADC_CH); // flow meter raw value reading from ADS1115

  press1_bar = get_pressure(ADS.toVoltage(pt1_raw_volt)); // bar
  press2_bar = get_pressure(ADS.toVoltage(pt2_raw_volt)); // bar
  FM_g_per_s = get_flow(ADS.toVoltage(fm_raw_volt)); // g/s

  temp_1_degC = tc1.readTempC(); // degC
  temp_2_degC = tc2.readTempC(); // degC

  // Print in CSV format into the serial.
  Serial.print(time);
  Serial.print(",");
  Serial.print(press1_bar);
  Serial.print(",");
  Serial.print(press2_bar);
  Serial.print(",");
  Serial.print(FM_g_per_s);
  Serial.print(",");
  Serial.print(temp_1_degC);
  Serial.print(",");
  Serial.println(temp_2_degC);
}