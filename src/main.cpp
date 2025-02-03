#include "daq_setting.h"

static unsigned long last_print_time = 0;

void setup() {
  // Setup Serial Communication b.t. Teensy and Computer
  Serial.begin(SERIAL_BAUDRATE);

  // Setup ADS1115 for PT sensor analog reading
  Wire.begin();
  ADS.begin();
  ADS.setGain(1); // 4.096 Volt
  ADS.setDataRate(7);
  ADS.readADC(0);

  Serial.println(F("DAQ is ready."));
}

void loop() {
  /* Sensor update part. */
  /*******************************************************************/
  unsigned long current_time = millis();
  // Update every SENSOR_RATE time.
  if (current_time - last_print_time >= SENSOR_RATE) {
    print_value_to_serial(current_time);
    last_print_time = current_time;
  }
  
  /*******************************************************************/
}
