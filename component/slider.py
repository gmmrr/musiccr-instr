from gpiozero import MCP3008
import time


class Slider():
    def __init__(self):
        self.state = 3

        self.adc = MCP3008(channel=0)

    def get_state(self):
        return self.state


class PitchSlider(Slider):
    def __init__(self):
        super().__init__()

    def update(self):
        self.state = self.adc.value
        time.sleep(0.5)
        return True
