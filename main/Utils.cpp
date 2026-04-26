#include "Utils.h"

void roambaPrintTime(void) 
{
    double time = (double)millis() / 1000;
    Serial.print("[");
    Serial.print(time, 8);
    Serial.print("]\t");
}