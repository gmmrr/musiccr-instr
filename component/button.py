import RPi.GPIO as GPIO
import time
import threading

class Button:
    def __init__(self, pin):
        self.pin = pin
        self.e_press = threading.Event()

        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.pin, GPIO.FALLING, callback=self.pressed, bouncetime=200)

    def pressed(self, channel):
        self.e_press.set()

    def wait(self):
        self.e_press.wait()
        self.e_press.clear()
