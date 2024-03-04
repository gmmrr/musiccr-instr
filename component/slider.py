import smbus
import time


class Slider():
    def __init__(self):
        self.state = 3

        self.address = 0x48
        self.bus = smbus.SMBus(1)

        self.bus.write_byte(self.address, 0)



    def get_state(self):
        return self.state


class PitchSlider(Slider):
    def __init__(self):
        super().__init__()

    def update(self):
        value = self.bus.read_byte(self.address)
        self.state = ((value - 1) // 51) + 1


        time.sleep(0.1)
        return True
