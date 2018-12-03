
#include "FastLED.h"

#include "SoftwareSerial.h"
#include "Adafruit_Pixie.h"

#define NUMPIXELS 3 // Number of Pixies in the strip
#define PIXIEPIN 11 // Pin number for SoftwareSerial output

SoftwareSerial pixieSerial(-1, PIXIEPIN);

Adafruit_Pixie strip = Adafruit_Pixie(NUMPIXELS, &pixieSerial);
// Alternately, can use a hardware serial port for output, e.g.:
// Adafruit_Pixie strip = Adafruit_Pixie(NUMPIXELS, &Serial1);

void setup()
{
  int i;

  Serial.begin(9600);
  Serial.println("Ready to Pixie!");

  pixieSerial.begin(115200); // Pixie REQUIRES this baud rate
  // Serial1.begin(115200);  // <- Alt. if using hardware serial port

  strip.setBrightness(200); // Adjust as necessary to avoid blinding

  // Serial.println("Red!");
  // for(i=0; i< NUMPIXELS; i++)
  //   strip.setPixelColor(i, 255, 255, 255);
  // strip.show();
  /*  delay(300);

  Serial.println("Green!");
  for(i=0; i< NUMPIXELS; i++)
    strip.setPixelColor(i, 0, 255, 0);
  strip.show();
  delay(300);

  Serial.println("Blue!");
  for(i=0; i< NUMPIXELS; i++)
    strip.setPixelColor(i, 0, 0, 255);
  strip.show();
  delay(300);*/
}

void loop()
{
  // int i;
  // for(i=0; i< NUMPIXELS; i++)
  //   strip.setPixelColor(i, 200, 0, 0);
  // strip.show();
  // delay(5);
  // Serial.println("Rainbow!");
  rainbowCycle(10);
}

// Slightly different, this makes the rainbow equally distributed throughout
unsigned long lastAmbientCycle = 0;

void ambientCycle(uint8_t wait)
{
  unsigned long now = millis();
  if (now - lastAmbientCycle < 10)
    return;

  lastAmbientCycle = now;

  uint16_t i, j;
  uint16_t h = beatsin8(10, 0, 255);

  uint16_t h_final = 80 + sin8(h + j) / 16;

  for (i = 0; i < NUMPIXELS; i++)
  {
    strip.setPixelColor(i, hsv2rgb(h_final, 200, 250));
  }
  strip.show();
}

void rainbowCycle(uint8_t wait)
{
  unsigned long now = millis();
  if (now - lastAmbientCycle < 100)
    return;

  lastAmbientCycle = now;

  uint16_t i, j;
  j =  beatsin8(20, 0, 255);
  for (i = 0; i < NUMPIXELS; i++)
  {
    strip.setPixelColor(i, Wheel(((i * 256 / strip.numPixels()) + j) & 255));
  }
  strip.show();
}

// Input a value 0 to 255 to get a color value.
// The colours are a transition r - g - b - back to r.
uint32_t Wheel(byte WheelPos)
{
  if (WheelPos < 85)
  {
    return strip.Color(WheelPos * 3, 255 - WheelPos * 3, 0);
  }
  else if (WheelPos < 170)
  {
    WheelPos -= 85;
    return strip.Color(255 - WheelPos * 3, 0, WheelPos * 3);
  }
  else
  {
    WheelPos -= 170;
    return strip.Color(0, WheelPos * 3, 255 - WheelPos * 3);
  }
}

uint32_t hsv2rgb(int32_t h, uint8_t s, uint8_t v)
{
  uint8_t n, r, g, b;

  // Hue circle = 0 to 1530 (NOT 1536!)
  h %= 1530; // -1529 to +1529
  if (h < 0)
    h += 1530; //     0 to +1529
  n = h % 255; // Angle within sextant; 0 to 254 (NOT 255!)
  switch (h / 255)
  { // Sextant number; 0 to 5
  case 0:
    r = 255;
    g = n;
    b = 0;
    break; // R to Y
  case 1:
    r = 254 - n;
    g = 255;
    b = 0;
    break; // Y to G
  case 2:
    r = 0;
    g = 255;
    b = n;
    break; // G to C
  case 3:
    r = 0;
    g = 254 - n;
    b = 255;
    break; // C to B
  case 4:
    r = n;
    g = 0;
    b = 255;
    break; // B to M
  default:
    r = 255;
    g = 0;
    b = 254 - n;
    break; // M to R
  }

  uint32_t v1 = 1 + v;  // 1 to 256; allows >>8 instead of /255
  uint16_t s1 = 1 + s;  // 1 to 256; same reason
  uint8_t s2 = 255 - s; // 255 to 0

  r = ((((r * s1) >> 8) + s2) * v1) >> 8;
  g = ((((g * s1) >> 8) + s2) * v1) >> 8;
  b = ((((b * s1) >> 8) + s2) * v1) >> 8;

  return ((uint32_t)r << 16) | ((uint16_t)g << 8) | b;
}