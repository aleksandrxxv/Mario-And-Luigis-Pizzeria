#include <Display.h>

const int buzzerPin = 3;           // Pin connected to the buzzer
const int startTime = 10;         // Countdown time in seconds (10 minutes)
int countdownTime = startTime;     // Variable to store remaining time

bool countdownActive = false;      // Flag to track if countdown is active

void setup() {
    Serial.begin(9600);            // Initialize serial communication          
    Display.clear();               // Clear the display
    pinMode(buzzerPin, OUTPUT);    // Set buzzer pin as output
}

void loop() {
    // Check for serial input
    if (Serial.available() > 0) {
        String command = Serial.readStringUntil('\n');  // Read command from Flask

        if (command == "START_TIMER" && !countdownActive) {    // Start countdown if not already active
            countdownTime = startTime;                  // Reset countdown time
            countdownActive = true;                     // Activate countdown
        }
    }

    // Countdown logic
    if (countdownActive && countdownTime > 0) {
        Display.clear();
        Display.show(countdownTime);    // Display remaining seconds
        delay(1000);                     // Wait for one second
        countdownTime--;                 // Decrease the countdown by one second
    }

    // When countdown reaches zero
    if (countdownActive && countdownTime == 0) {
        Display.clear();
        Display.show("0");              // Display "0" when time is up
        tone(buzzerPin, 1000, 1000);     // Play buzzer at 1000 Hz for 1 second
        Serial.println("DONE");         // Send a message back to Flask
        countdownActive = false;         // Deactivate countdown
    }
}
