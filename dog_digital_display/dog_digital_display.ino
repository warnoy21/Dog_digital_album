/*
Details: Cycle thru seven photos to display on a TFT round lcd using ESP-32

DAte : June 1 2025        Made by: Aaron Gumba        Initial Creation



*/
#include <PNGdec.h>
#include "photos.h" 

PNG png;
#define MAX_IMAGE_WIDTH 240

int16_t xpos = 0;
int16_t ypos = 0;

#include "SPI.h"
#include <TFT_eSPI.h>             
TFT_eSPI tft = TFT_eSPI();        

// Array of image pointers
const uint8_t* images[] = { photo1,photo2,photo3,photo4,photo5,photo6,photo7};
const size_t imageSizes[] = { sizeof(photo1),sizeof(photo2),sizeof(photo3),sizeof(photo4),
                              sizeof(photo5),sizeof(photo6),sizeof(photo7), };
const int numImages = sizeof(images) / sizeof(images[0]);

// Callback function to draw pixels to the display
void pngDraw(PNGDRAW *pDraw) {
  uint16_t lineBuffer[MAX_IMAGE_WIDTH];
  png.getLineAsRGB565(pDraw, lineBuffer, PNG_RGB565_LITTLE_ENDIAN, 0xffffffff);

  for (int x = 0; x < pDraw->iWidth; x++) {
    tft.drawPixel(
      xpos + pDraw->y,
      ypos + (png.getWidth() - 1 - x),
      lineBuffer[x]
    );
  }
}





void setup() {
//  Serial.begin(115200);
 // Serial.println("\n\nUsing the PNGdec library");
  
  tft.begin();
  tft.fillScreen(TFT_BLACK);

}

void loop() {

  for (int i = 0; i < numImages; i++) {
  
    int16_t rc = png.openFLASH((uint8_t*)images[i], imageSizes[i], pngDraw);  // Explicit cast

    if (rc == PNG_SUCCESS) {
      
      tft.startWrite();
      uint32_t dt = millis();
      png.decode(NULL, 0);
      Serial.printf("%d ms\n", millis() - dt);
      tft.endWrite();
    }

    delay(5000);  // Wait before displaying the next image
  }
}



