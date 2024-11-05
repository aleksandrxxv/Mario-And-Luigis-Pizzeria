#include <Display.h>

const int buzzerPin = 3;
const int startTime = 10;
int countdownTime = startTime;

bool countdownActive = false;

void setup() {
    Serial.begin(9600);      
    Display.clear();
    pinMode(buzzerPin, OUTPUT);
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
        tone(buzzerPin, 1000, 1000);
        Serial.println("DONE");
        countdownActive = false;
    }
}
