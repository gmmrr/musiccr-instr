import RPi.GPIO as GPIO
import time

class PlayButton():
    def __init__(self, pin):
        self.pin = pin

        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)


    def wait(self):

        while True:
            if GPIO.input(self.pin) == GPIO.LOW:
                break
