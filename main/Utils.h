#ifndef UTILS_H
#define UTILS_H

#include <Arduino.h>

// Function to pretty print a timestamp before regular Serial.print calls
void roambaPrintTime(void);

// Helper class to make easy "breakpoints" to check
// whether sections of code are hit during debugging
class BreakPoint {
    private:
        uint8_t bpID;
    public:
        // Constructor
        BreakPoint(uint8_t id) {
            bpID = id; 
        }

        print() {
            roambaPrintTime();
            Serial.print("Breakpoint ");
            Serial.println(bpID);
        }
};

#endif