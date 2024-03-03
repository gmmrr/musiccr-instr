import smbus
import time


class Slider():
    def __init__(self):
        self.state = 3

        self.address = 0x48
        self.bus = smbus.SMBus(1)
        self.bus.write_byte(self.address, 0)

        self.set_breakpnt()


    def set_breakpnt(self):
        self.breakpnt_1 = 51
        self.breakpnt_2 = 102
        self.breakpnt_3 = 154
        self.breakpnt_4 = 205


    def get_state(self):
        return self.state


class PitchSlider(Slider):
    def __init__(self):
        super().__init__()

    def update(self):
        value = self.bus.read_byte(self.address)

        if   value < self.breakpnt_1:
            self.state = 1
        elif value < self.breakpnt_2:
            self.state = 2
        elif value < self.breakpnt_3:
            self.state = 3
        elif value < self.breakpnt_4:
            self.state = 4
        else:
            self.state = 5

        time.sleep(0.1)
        return True
