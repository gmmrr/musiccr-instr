from gpiozero import MCP3008
import smbus
import time


class Slider():
    def __init__(self):
        self.state = 3

        self.adc = MCP3008(channel=0)

        self.address = 0x48
        self.A0 = 0x40
        self.A1 = 0x41
        self.A2 = 0x42
        self.A3 = 0x43
        self.bus = smbus.SMBus(0)


    def get_state(self):
        return self.state


class PitchSlider(Slider):
    def __init__(self):
        super().__init__()

    def update(self):
        self.state = self.adc.value

        self.bus.write_byte(self.address, self.A0)
        value = self.bus.read_byte(self.address)
        print(f"AOUT: {value}")

        time.sleep(0.5)
        return True
