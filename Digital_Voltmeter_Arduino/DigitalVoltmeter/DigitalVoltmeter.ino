#include <LiquidCrystal.h>

LiquidCrystal lcd(9, 8, 5, 4, 3, 2); // Adjust the pin numbers as per your wiring

const int analogPin = A0; // Pin A0 is used as the analog input
const float referenceVoltage = 5.0; // Your reference voltage in volts

void setup() {
  lcd.begin(16, 2); // Initialize the LCD with 16 columns and 2 rows
  lcd.print("DYK team");
}

void loop() {
  // Read the analog value from pin A0
  int analogValue = analogRead(analogPin);

  // Convert the analog value to volts
  float voltage = (analogValue / 1023.0) * referenceVoltage;

  // Display the voltage on the LCD
  lcd.setCursor(0, 1); // Move cursor to the second row
  lcd.print("Voltage: ");
  lcd.print(voltage, 2); // Display the voltage with 2 decimal places
  lcd.print(" V");

  delay(1000); // Delay between updates (adjust as needed)
}
