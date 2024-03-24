import smbus
import time

class Slider():
    def __init__(self):
        self.state = 3

        self.address = 0x48
        self.bus = smbus.SMBus(1)
        self.bus.write_byte(self.address, 0)

        # set breakpoint
        self.breakpoint_1 = 51
        self.breakpoint_2 = 102
        self.breakpoint_3 = 154
        self.breakpoint_4 = 205

        self.last_state = self.state


    def get_state(self):
        return self.state


class PitchSlider(Slider):
    def __init__(self):
        super().__init__()

    def update(self):
        value = self.bus.read_byte(self.address)

        if   value < self.breakpoint_1:
            self.state = 1
        elif value < self.breakpoint_2:
            self.state = 2
        elif value < self.breakpoint_3:
            self.state = 3
        elif value < self.breakpoint_4:
            self.state = 4
        else:
            self.state = 5


        if self.state != self.last_state:
            self.last_state = self.state
            return True
        else:
            return False
