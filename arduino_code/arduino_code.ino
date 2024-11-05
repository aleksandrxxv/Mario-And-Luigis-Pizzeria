#include <Display.h>

const int buzzerPin = 3;
const int startTime = 10;
const int PIN_LED = 4; // The Number of the red LED pin
int countdownTime = startTime;

bool countdownActive = false;

void setup() {
    Serial.begin(9600);      
    Display.clear();
    pinMode(buzzerPin, OUTPUT);
    pinMode(PIN_LED, OUTPUT);
}

void loop() {
    if (Serial.available() > 0) {
        String command = Serial.readStringUntil('\n');

        if (command == "START_TIMER" && !countdownActive) {
            countdownTime = startTime;
            countdownActive = true;
        }
    }

    if (countdownActive && countdownTime > 0) {
        Display.clear();
        Display.show(countdownTime);
        delay(1000);
        countdownTime--;
    }

    if (countdownActive && countdownTime == 0) {
        Display.clear();
        Display.show("0");
        digitalWrite(PIN_LED, HIGH);
        delay(500);
        digitalWrite(PIN_LED, LOW);
        delay(500);
        digitalWrite(PIN_LED, HIGH);
        delay(500);
        digitalWrite(PIN_LED, LOW);
        delay(500);
        digitalWrite(PIN_LED, HIGH);
        delay(500);
        digitalWrite(PIN_LED, LOW);
        tone(buzzerPin, 1000, 1000);
        Serial.println("DONE");
        countdownActive = false;
    }
}
