#include <Arduino.h>

// Program for Arduino Mega 2560 R3
// It can be easily adapted to other Arduino models

const int pwmPin1 = 2;      // PWM pin 1
const int pwmPin2 = 3;      // PWM pin 2
const int pwmPin3 = 4;      // PWM pin 3
const int pwmPin4 = 5;      // PWM pin 4

const int analogPin1 = A0;  // Analog pin 1
const int analogPin2 = A1;  // Analog pin 2
const int analogPin3 = A2;  // Analog pin 3
const int analogPin4 = A3;  // Analog pin 4
const int pwmFrequency = 1500;  // PWM frequency in Hz

int dutyCycle1 = 0;         // Duty cycle for PWM pin 1
int dutyCycle2 = 0;         // Duty cycle for PWM pin 2
int dutyCycle3 = 0;         // Duty cycle for PWM pin 3
int dutyCycle4 = 0;         // Duty cycle for PWM pin 4

void setup() {
  // Set the PWM frequency for pins 2 to 13 (Timer1)
  TCCR1B = (TCCR1B & 0xF8) | 0x01;  // Set Timer1 prescaler to 1 (no prescaling)

  // Set the PWM frequency for pins 44 to 46 (Timer5)
  TCCR5B = (TCCR5B & 0xF8) | 0x01;  // Set Timer5 prescaler to 1 (no prescaling)

  pinMode(pwmPin1, OUTPUT);
  pinMode(pwmPin2, OUTPUT);
  pinMode(pwmPin3, OUTPUT);
  pinMode(pwmPin4, OUTPUT);
  
  // Initialize serial communication
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    // Read new duty cycle values from the serial port
    dutyCycle1 = Serial.parseInt();
    dutyCycle2 = Serial.parseInt();
    dutyCycle3 = Serial.parseInt();
    dutyCycle4 = Serial.parseInt();
    
    // Set the new duty cycles for the PWM pins
    analogWrite(pwmPin1, dutyCycle1);
    analogWrite(pwmPin2, dutyCycle2);
    analogWrite(pwmPin3, dutyCycle3);
    analogWrite(pwmPin4, dutyCycle4);
    delay(100);
  }
    
  // Read analog values from the analog pins
  int analogValue1 = analogRead(analogPin1);
  int analogValue2 = analogRead(analogPin2);
  int analogValue3 = analogRead(analogPin3);
  int analogValue4 = analogRead(analogPin4);
  delay(100);
  
  // Send analog values over the serial connection
  Serial.print(analogValue1);
  Serial.print(",");
  Serial.print(analogValue2);
  Serial.print(",");
  Serial.print(analogValue3);
  Serial.print(",");
  Serial.println(analogValue4);
  delay(200);
  }