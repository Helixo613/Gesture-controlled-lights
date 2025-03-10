#define LED_COUNT 5
const int ledPins[LED_COUNT] = {2, 4, 8, 10, 12};

unsigned long previousMillis = 0; // Store the last time LEDs were updated
const long interval = 100; // Interval for checking serial input (in milliseconds)

void setup() {
  Serial.begin(9600); // Initialize serial communication at 9600 bits per second
  for (int i = 0; i < LED_COUNT; i++) {
    pinMode(ledPins[i], OUTPUT);
  }
  Serial.println("Setup complete.");
}

void loop() {
  unsigned long currentMillis = millis();

  // Check for serial input every 'interval' milliseconds
  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis; // Save the last time we checked for input

    if (Serial.available() > 0) {
      String msg = Serial.readStringUntil('\n'); // Read until newline
      Serial.print("Received message: ");
      Serial.println(msg);
      
      if (msg.startsWith("ZERO") || msg.startsWith("0")) {
        setLEDs(0);
        Serial.println("All LEDs off");
      } else if (msg.startsWith("ONE")) {
        setLEDs(1);
        Serial.println("LED 1 on");
      } else if (msg.startsWith("TWO")) {
        setLEDs(2);
        Serial.println("LED 1 and 2 on");
      } else if (msg.startsWith("THREE")) {
        setLEDs(3);
        Serial.println("LED 1, 2, and 3 on");
      } else if (msg.startsWith("FOUR")) {
        setLEDs(4);
        Serial.println("LED 1, 2, 3, and 4 on");
      } else if (msg.startsWith("FIVE")) {
        setLEDs(5);
        Serial.println("All LEDs on");
      } else {
        Serial.println("Unknown message");
      }
    }
  }
}

void setLEDs(int count) {
  for (int i = 0; i < LED_COUNT; i++) {
    if (i < count) {
      digitalWrite(ledPins[i], HIGH);
    } else {
      digitalWrite(ledPins[i], LOW);
    }
  }
}