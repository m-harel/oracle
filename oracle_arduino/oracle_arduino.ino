#include "FastLED.h"
#include "SoftwareSerial.h"
#include "Adafruit_Pixie.h"

#define AMBIENT_LIGHT_BYTE 89
#define PARTY_LIGHT_BYTE 167
#define WAIT_FOR_ANSWER_BYTE 65

enum STATE_TYPE
{
  AMBIENT,
  PARTY,
  WAIT_FOR_ANSWER
};

const int buttonPin = 4;  // "Button 1"
const int togglePINT = 2; // "Button 2"
unsigned long last_message_send = 0;

#define LED_PIN 9
#define NUM_LEDS 20
#define PIXIE_NUM 4
#define BRIGHTNESS 64
#define LED_TYPE WS2811
#define COLOR_ORDER GRB


#define NUMPIXELS 3 // Number of Pixies in the strip
#define PIXIEPIN  11 // Pin number for SoftwareSerial output


SoftwareSerial pixieSerial(-1, PIXIEPIN);

Adafruit_Pixie strip = Adafruit_Pixie(NUMPIXELS, &pixieSerial);


CRGB leds[NUM_LEDS];

#define UPDATES_PER_SECOND 100

CRGBPalette16 currentPalette;
TBlendType currentBlending;

extern CRGBPalette16 myRedWhiteBluePalette;
extern const TProgmemPalette16 myRedWhiteBluePalette_p PROGMEM;

STATE_TYPE state = AMBIENT;

void setup()
{                                   //setup the system
  Serial.begin(9600);               //establish a serial communication
  pinMode(buttonPin, INPUT_PULLUP); //set buttonPin as input with pullup resistor
  delay(3000);                      // power-up safety delay
  FastLED.addLeds<LED_TYPE, LED_PIN, COLOR_ORDER>(leds, NUM_LEDS).setCorrection(TypicalLEDStrip);
  FastLED.setBrightness(BRIGHTNESS);

  pixieSerial.begin(115200); // Pixie REQUIRES this baud rate
  strip.setBrightness(200);  // Adjust as necessary to avoid blinding
  

  currentPalette = RainbowColors_p;
  currentBlending = LINEARBLEND;

  setAmbientLight();
  // setPartyLight();
}

void loop()
{
  process_state();
  check_button();
  check_state_change();

 for(int i=0; i< NUMPIXELS; i++)
    strip.setPixelColor(i, 200, 200, 200);
  strip.show();
}

void process_state()
{
  switch (state)
  {
  case AMBIENT:
    process_ambient();
    break;
  case PARTY:
    process_party();
    break;
  case WAIT_FOR_ANSWER:
    process_wait();
    break;
  }
}

void process_ambient()
{
  sinelon();

  FastLED.show();
}

uint8_t gHue = 0; // rotating "base color"

void rainbowWithGlitter()
{

  // do some periodic updates
  EVERY_N_MILLISECONDS(20) { gHue++; } // slowly cycle the "base color" through the rainbow
  EVERY_N_MILLISECONDS(5)
  { // built-in FastLED rainbow, plus some random sparkly glitter
    rainbow();
    addGlitter(80);
  }
}

void rainbow()
{
  // FastLED's built-in rainbow generator
  fill_rainbow(leds, NUM_LEDS, gHue, 7);
}

void addGlitter(fract8 chanceOfGlitter)
{
  if (random8() < chanceOfGlitter)
  {
    leds[random16(NUM_LEDS)] += CRGB::White;
  }
}

void process_party()
{
  static uint8_t startIndex = 0;
  startIndex = startIndex + 1; /* motion speed */

  // PixeRainbowCycle();
  rainbowWithGlitter();
  FastLED.show();
}

void process_wait()
{
  static uint8_t startIndex = 0;
  startIndex = startIndex + 1; /* motion speed */

  FillLEDsFromPaletteColors(startIndex);

  FastLED.show();
}

void check_button()
{
  int buttonState = digitalRead(buttonPin);
  if (buttonState == 0)
  {
    unsigned long now = millis();
    if (now - last_message_send < 100)
      return;
    Serial.println("k");
    last_message_send = millis();
  }
}

void check_state_change()
{
  while (Serial.available() > 0)
  {
    int temp = Serial.read();
    switch (temp)
    {
    case AMBIENT_LIGHT_BYTE:
      setAmbientLight();
      break;
    case PARTY_LIGHT_BYTE:
      setPartyLight();
      break;
    case WAIT_FOR_ANSWER_BYTE:
      setWaitLight();
      break;
    default:
      continue;
    }
    flush_serial();
  }
}

void sinelon()
{
  uint16_t h = beatsin8(10, 0, 255);
  for (int i; i < NUM_LEDS; i++)
  {
    uint16_t h_final =  80+sin8(h+i)/16;
    uint8_t brightness = beatsin8(16, 120, 224);
    leds[i] = CHSV(h_final, 250, brightness);
  }
  FastLED.show();
}

void setAmbientLight()
{
  state = AMBIENT;
  currentPalette = CloudColors_p;
  currentBlending = LINEARBLEND;
}

void setPartyLight()
{
  state = PARTY;
  currentPalette = PartyColors_p;
  currentBlending = LINEARBLEND;
}

void setWaitLight()
{
  state = WAIT_FOR_ANSWER;
  currentPalette = RainbowStripeColors_p;
  currentBlending = NOBLEND;
}

void flush_serial()
{ //error handler
  delay(5);

  while (Serial.available())
  {
    Serial.read();
    delay(1);
  }
}

/////////

void FillLEDsFromPaletteColors(uint8_t colorIndex)
{
  uint8_t brightness = 150;

  for (int i = 0; i < NUM_LEDS; i++)
  {
    leds[i] = ColorFromPalette(currentPalette, colorIndex, brightness, currentBlending);
    colorIndex += 1;
  }
}

// This function fills the palette with totally random colors.
void SetupTotallyRandomPalette()
{
  for (int i = 0; i < 16; i++)
  {
    currentPalette[i] = CHSV(random8(), 255, random8());
  }
}

// This function sets up a palette of black and white stripes,
// using code.  Since the palette is effectively an array of
// sixteen CRGB colors, the various fill_* functions can be used
// to set them up.
void SetupBlackAndWhiteStripedPalette()
{
  // 'black out' all 16 palette entries...
  fill_solid(currentPalette, 16, CRGB::Black);
  // and set every fourth one to white.
  currentPalette[0] = CRGB::White;
  currentPalette[4] = CRGB::White;
  currentPalette[8] = CRGB::White;
  currentPalette[12] = CRGB::White;
}

// This function sets up a palette of purple and green stripes.
void SetupPurpleAndGreenPalette()
{
  CRGB purple = CHSV(HUE_PURPLE, 255, 255);
  CRGB green = CHSV(HUE_GREEN, 255, 255);
  CRGB black = CRGB::Black;

  currentPalette = CRGBPalette16(
      green, green, black, black,
      purple, purple, black, black,
      green, green, black, black,
      purple, purple, black, black);
}

// This example shows how to set up a static color palette
// which is stored in PROGMEM (flash), which is almost always more
// plentiful than RAM.  A static PROGMEM palette like this
// takes up 64 bytes of flash.
const TProgmemPalette16 myRedWhiteBluePalette_p PROGMEM =
    {
        CRGB::Red,
        CRGB::Gray, // 'white' is too bright compared to red and blue
        CRGB::Blue,
        CRGB::Black,

        CRGB::Red,
        CRGB::Gray,
        CRGB::Blue,
        CRGB::Black,

        CRGB::Red,
        CRGB::Red,
        CRGB::Gray,
        CRGB::Gray,
        CRGB::Blue,
        CRGB::Blue,
        CRGB::Black,
        CRGB::Black};

// Slightly different, this makes the rainbow equally distributed throughout
void PixeRainbowCycle()
{
  // uint16_t i;

  // for (i = 0; i < PIXIE_NUM; i++)
  // {
  //   strip.setPixelColor(i, PixieWheel(((i * 256 / strip.numPixels()) + beatsin8(10)) & 255));
  // }
  // strip.show();
}

// Input a value 0 to 255 to get a color value.
// The colours are a transition r - g - b - back to r.
uint32_t PixieWheel(byte WheelPos)
{
  // if (Pos < 85)
  // {
  //   return strip.Color(WheelPos * 3, 255 - WheelPos * 3, 0);
  // }
  // else if (WheelPos < 170)
  // {
  //   WheelPos -= 85;
  //   return strip.Color(255 - WheelPos * 3, 0, WheelPos * 3);
  // }
  // else
  // {
  //   WheelPos -= 170;
  //   return strip.Color(0, WheelPos * 3, 255 - WheelPos * 3);
  // }
}
