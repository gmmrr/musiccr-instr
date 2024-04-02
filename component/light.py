import time
from rpi_ws281x import Adafruit_NeoPixel, Color


class Light():
    def __init__(self, pin):
        self.pin = pin

        self.reset()

        self.is_updating = False
        self.music = "src/s3m3.mp3"
        self.volume = 50


    def reset(self):

        # Define the basic settings of the LED strip
        self.LED_COUNT = 40 # Number of LED pixels.
        self.LED_PIN = self.pin # GPIO pin connected to the pixels (18 uses PWM!).
        self.LED_FREQ_HZ = 800000 # LED signal frequency in hertz (usually 800khz)
        self.LED_DMA = 10 # DMA channel to use for generating signal (try 10)
        self.LED_BRIGHTNESS = 255 # Set to 0 for darkest and 255 for brightest
        self.LED_INVERT = False # True to invert the signal (when using NPN transistor level shift)
        self.LED_CHANNEL = 0 # set to '1' for GPIOs 13, 19, 41, 45 or 53

        # Create NeoPixel and put all settings in
        self.strip = Adafruit_NeoPixel(
            self.LED_COUNT,
            self.LED_PIN,
            self.LED_FREQ_HZ,
            self.LED_DMA,
            self.LED_INVERT,
            self.LED_BRIGHTNESS,
            self.LED_CHANNEL
        )

        # Initialize the library
        self.strip.begin()  # must be called before any operation



    def update(self, music, volume):
        self.music = music
        self.volume = volume

        self.is_updating = True


    def turn_on(self):

        # while True:
            for i in range(0,self.LED_COUNT):
                self.strip.setPixelColor(i, Color(100, 100, 100))
            self.strip.show()
            print("light on")

        #     if self.is_updating:
        #         break
        #
        # self.is_updating = False


    def turn_off(self):
        for i in range(0,self.LED_COUNT):
            self.strip.setPixelColor(i, Color(0, 0, 0))
        self.strip.show()






#------------------------------------
# this should be put inside main.py
#------------------------------------

# def light_thread():
#     '''
#     To deal with the light effect
#
#     '''
#
#     global is_working
#     global is_music_updated
#     global is_volume_updated
#     global val_music
#     global val_volume
#     global pin_led
#
#
#     light_obj = light.Light(pin = pin_led)
#     light_obj.update(val_music, val_volume)
#
#     # while True:
#     #     while is_working:
#     #
#     #         if is_music_updated or is_volume_updated:
#     #             light.update(val_music, val_volume)
#     #             time.sleep(0.05)
#     #             is_music_updated = False
#     #             is_volume_updated = False
#
#     t_light_turn_on = threading.Thread(target=light_obj.turn_on)
#     t_light_turn_on.start()
#
#     t_light_turn_on = threading.Thread(target=light_obj.turn_on)
#     t_light_turn_on.start()
#
#
#         # light_obj.turn_off()
