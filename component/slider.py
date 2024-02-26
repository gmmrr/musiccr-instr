import RPi.GPIO as GPIO
import time


class Slider():
    def __init__(self, pin):
        self.pin = pin
        self.state = 3

        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def get_state(self):
        return self.state

class PitchSlider(Slider):
    def __init__(self, pin):
        # derive from Slider class
        super().__init__(pin)

    def update(self):
        self.state = GPIO.input(self.pin)
        return True
