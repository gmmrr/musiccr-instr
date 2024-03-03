from gpiozero import MCP3008
import smbus
import time


class Slider():
    def __init__(self):
        self.state = 3

        self.adc = MCP3008(channel=0)

        self.address = 0x48
        self.a0 = 0x40
        self.a1 = 0x41
        self.a2 = 0x42
        self.a3 = 0x43
        self.bus = smbus.SMBus(1)


    def get_state(self):
        return self.state


class PitchSlider(Slider):
    def __init__(self):
        super().__init__()

    def update(self):
        self.state = self.adc.value

        self.bus.write_byte(self.address, self.a0)
        value = self.bus.read_byte(self.address)
        print(f"AOUT: {value}")

        time.sleep(0.5)
        return True
