import time
from rpi_ws281x import PixelStrip, Color


class Light():
    def __init__(self, pin):
        self.pin = pin

        self.init()


    def init(self):
        LED_COUNT = 8
        LED_PIN = self.pin
        LED_FREQ_HZ = 800000
        LED_DMA = 10  # DMA 通道
        LED_BRIGHTNESS = 255
        LED_INVERT = False

        self.strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
        self.strip.begin()


    def turn_on(self):
        self.state = True
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, Color(255, 255, 255))
        self.strip.show()

    def turn_off(self):
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, Color(0, 0, 0))
        self.strip.show()
