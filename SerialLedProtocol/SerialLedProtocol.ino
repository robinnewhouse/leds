#include <FastLED.h>

#define NUM_LEDS 100
#define DATA_PIN 14
#define LED_TYPE WS2812B
#define DELAY 1000
#define SERIAL_PACKET_SIZE 500
#define TIMEOUT_MS 50

#define PIXEL_SET_PIXEL  0x03 // set the color value of pixel n using 32bit packed color value

#define BEGIN_COMMAND  0x0A
#define END_COMMAND 0x0B

CRGB leds[NUM_LEDS];

byte recieved_serial[SERIAL_PACKET_SIZE];
uint char_position;

void setup() {
  // initialize serial communication
  Serial.begin(57600);
  Serial.setTimeout(TIMEOUT_MS);

  // initialize pin type
  FastLED.addLeds<LED_TYPE, DATA_PIN, GRB>(leds, NUM_LEDS);
  FastLED.setBrightness(20);
  FastLED.clear();
  FastLED.show();
  char_position = 0;
}



//void handle_packet(byte* data) {
//
//  if (data[0] == BEGIN_COMMAND && data[5] == END_COMMAND) {
//    uint index = data[1];
//    uint color = ((data[2] << 16) | (data[3] << 8) | data[4]);
//    leds[index] = color;
//
//    FastLED.show();
//
//  }
//
//
//}

void debug(int i, int color) {

  leds[i] = color;
  FastLED.show();
}


int  serIn; //var that will hold the bytes in read from the serialBuffer
const uint8_t header[4] = { 0xDE, 0xAD, 0xBE, 0xEF };

void loop () {
  //simple feedback from Arduino  Serial.println("Hello World");

  // we're going to read led data directly from serial, after we get our header
  //  Serial.print("first byte recieved");

  if (Serial.available() > 0) {
//    Serial.println("Serial is available");

    uint8_t b = Serial.read();

    bool looksLikeHeader = false;
    if (b == header[0]) {
      looksLikeHeader = true;

      for (int i = 1; looksLikeHeader && (i < sizeof(header)); i++) {
        b = Serial.read();

        if (b != header[i]) {
          // whoops, not a match, this no longer looks like a header.
          looksLikeHeader = false;
//          debug(i, CRGB::Red);
//          FastLED.delay(500);
        Serial.print("Looks like a header");

        }
        else {
//          debug(i, CRGB::Green);
//          FastLED.delay(0);
        };
      }
    }

    if (looksLikeHeader) {

      char myBytes[NUM_LEDS*3];

      Serial.readBytes(myBytes,NUM_LEDS*3);
      
      // hey, we read all the header bytes!  Yay!  Now read the frame data
      int bytesRead = 0;
      int i = 0;
      while (bytesRead < (NUM_LEDS * 3)) {
        int r = myBytes[3*i];
        int g = myBytes[3*i+1];
        int b = myBytes[3*i+2];

        leds[i].setRGB(r, g, b);
        bytesRead += 3;
        i++;
      }

      FastLED.show();
    }

  }
    while (Serial.available() > 0) {
      Serial.read(); // flush serial buffer
    }

}


