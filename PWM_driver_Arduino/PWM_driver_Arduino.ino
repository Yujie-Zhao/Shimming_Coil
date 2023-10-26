// Define the PWM output pins
const int PWM_PIN_1 = 9;
const int PWM_PIN_2 = 10;

// Define the minimum and maximum duty cycle values
const int MIN_DUTY_CYCLE = 0;
const int MAX_DUTY_CYCLE = 255;

// Define the delay between each duty cycle change (in milliseconds)
const int DELAY_TIME = 10;

void setup() {
  // Initialize the PWM pins as OUTPUT
  pinMode(PWM_PIN_1, OUTPUT);
  pinMode(PWM_PIN_2, OUTPUT);
}

void loop() {
  // Loop from minimum duty cycle to maximum duty cycle
  for (int dutyCycle = MIN_DUTY_CYCLE; dutyCycle <= MAX_DUTY_CYCLE; dutyCycle++) {
    // Set the duty cycle for both PWM outputs
    analogWrite(PWM_PIN_1, dutyCycle);
    analogWrite(PWM_PIN_2, dutyCycle);
    
    // Delay to observe the duty cycle change
    delay(DELAY_TIME);
  }
  
  // Loop from maximum duty cycle back to minimum duty cycle
  for (int dutyCycle = MAX_DUTY_CYCLE; dutyCycle >= MIN_DUTY_CYCLE; dutyCycle--) {
    // Set the duty cycle for both PWM outputs
    analogWrite(PWM_PIN_1, dutyCycle);
    analogWrite(PWM_PIN_2, dutyCycle);
    
    // Delay to observe the duty cycle change
    delay(DELAY_TIME);
  }
}