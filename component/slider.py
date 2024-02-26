from gpiozero import MCP3008
import time


class Slider():
    def __init__(self, pin):
        self.pin = pin
        self.state = 3

        # GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        self.adc = MCP3008(channel=self.pin)

    def get_state(self):
        return self.state

class PitchSlider(Slider):
    def __init__(self, pin):
        # derive from Slider class
        super().__init__(pin)

    def update(self):
        self.state = self.adc.value
        return True
