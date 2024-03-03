from gpiozero import MCP3008
import time


class Slider():
    def __init__(self):
        self.state = 3

        self.adc = MCP3008(channel=0)

        self.adc_1 = MCP3008(channel=1)
        self.adc_2 = MCP3008(channel=2)
        self.adc_3 = MCP3008(channel=3)


    def get_state(self):
        return self.state


class PitchSlider(Slider):
    def __init__(self):
        super().__init__()

    def update(self):
        self.state = self.adc.value
        print(self.adc_1.value)
        print(self.adc_2.value)
        print(self.adc_3.value)
        time.sleep(0.5)
        return True
