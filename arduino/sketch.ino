#include "FastLED.h"

//TAG: LEDStripdefinitions
CRGB leds[60];
int ledlengths[1] = {60};
CRGB* ledarr = {leds};
//TAG: LEDStripdefinitions_end
struct pixelValue{
    byte r;
    byte g;
    byte b;
};
struct ledMessage{
    byte strip;
    byte brightness;
    struct pixelValue pixels[1022/3];
};



void controlPixels(struct ledMessage message, int bytesinbuffer){
    Serial.println(message.strip, DEC);
    int strip = message.strip;
    int pixelvaluesnum = (bytesinbuffer-1)/3;
    for(int i = 0; i<pixelvaluesnum; i++){
        if(i >= ledlengths[strip]){
            break;
        }

        leds[i].setRGB((int)message.pixels[i].r, (int)message.pixels[i].g, (int)message.pixels[i].b);
        Serial.print(i);
        Serial.print(message.pixels[i].r, DEC);
        Serial.print(message.pixels[i].g, DEC);
        Serial.print(message.pixels[i].b, DEC);
        Serial.println();
        FastLED.show();
    }

}

void setup(){
    Serial.begin(9600);
    Serial.setTimeout(100);
    //TAG: FastledStripAdditions
    FastLED.addLeds<NEOPIXEL, 9>(leds, 60);
    //TAG: FastledStripAdditions_end
}

void loop(){
    //char buffer[1024];
    struct ledMessage message;
    memset(&message, 0, sizeof(ledMessage));
    int serial_f = Serial.readBytesUntil('\n', (byte*)&message, 1024);
    if(serial_f != 0){
        // we received a message to control neopixels
        controlPixels(message, serial_f);
    }
    delay(50);
    leds[0].setRGB(0, 0, 0);
    FastLED.show();
    delay(50);
    /*for(int i = 0; i<60; i++){
        leds[i] = CRGB::White;
    }
    FastLED.show();
    delay(50);
        for(int i = 0; i<60; i++){
        leds[i] = CRGB::Black;
    }
    FastLED.show();
    delay(50);*/
}

