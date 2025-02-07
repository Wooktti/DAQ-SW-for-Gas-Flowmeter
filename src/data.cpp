#include "daq_setting.h"

ADS1115 ADS(ADS1115_ADDR);

// 4~20mA = 0~200 slm (standard liter per minute)
float get_flow(float voltage) {
  // Convert voltage to current (in mA)
  float current = voltage / R_MAGNITUDE * 1000.0; // mA
  return ((current - 4.0) * 200 / 16.0); // slm
}

void print_value_to_serial(unsigned long time) {
  float FM_slm;
  int16_t fm_raw_volt;

  fm_raw_volt = ADS.readADC(FM_ADC_CH); // flow meter raw value reading from ADS1115
  FM_slm = get_flow(ADS.toVoltage(fm_raw_volt)); // slm

  if (MONITOR_METHOD) {
    // Print in CSV format into the serial.
    byte buf[8] = {0};
    memcpy(buf, &time, 4);
    memcpy(buf + 4, &FM_slm, 4);
    Serial.write(buf, 8);

  } else {
    // To use serial monitor, use the following code instead.
    Serial.print(time);
    Serial.print(",");
    Serial.println(FM_slm);
  }
}