const int analogPin = A0; // Pin A0 is used as the analog input

void setup() {
  Serial.begin(9600); // Initialize the serial communication
}

void loop() {
  int sensorValue = analogRead(analogPin); // Read the analog value from pin A0
  Serial.println(sensorValue); // Send the value to the Serial monitor
  delay(500); // Add a small delay before taking the next reading
}
