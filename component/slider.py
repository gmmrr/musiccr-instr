import RPi.GPIO as GPIO
import time


class Slider():
    def __init__(self, pin):
        self.pin = pin
        self.state = 3

        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def get_state(self):
        return self.state


class PitchSlider(Slider):
    def __init__(self, pin):
        super().__init__(pin)

    def update(self):
        self.state = GPIO.input(self.pin)
        time.sleep(0.5)
        return True
