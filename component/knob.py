import RPi.GPIO as GPIO
import time
import math


# Main Function
class Knob():
    def __init__(self, clk_pin, dt_pin):
        self.clk_pin = clk_pin
        self.dt_pin = dt_pin

        GPIO.setup(self.clk_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.dt_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def get_state(self):
        return self.current_state


class VolumeKnob(Knob):
    def __init__(self, clk_pin, dt_pin):
        super().__init__(clk_pin, dt_pin)

        self.current_state = 50
        self.clk_last_state = 50 # in units of the number(counter)

    def update(self):
        clk_state = GPIO.input(self.clk_pin)
        dt_state = GPIO.input(self.dt_pin)

        if clk_state != self.clk_last_state:
            self.current_state += 1 if dt_state != clk_state else -1

        if self.current_state > 100:
            self.current_state = 100
        elif self.current_state < 0:
            self.current_state = 0

        is_changed = clk_state != self.clk_last_state
        self.clk_last_state = clk_state
        return is_changed




class BPMKnob(Knob):
    def __init__(self, clk_pin, dt_pin):
        super().__init__(clk_pin, dt_pin)
        self.deadzone = 4

        self.current_state = 3
        self.current_temp_state = 50
        self.clk_last_state = 50 # in units of the number(counter)

    def update(self):
        clk_state = GPIO.input(self.clk_pin)
        dt_state = GPIO.input(self.dt_pin)

        if clk_state != self.clk_last_state:
            self.current_temp_state += 1 if dt_state != clk_state else -1

        if self.current_temp_state > 100:
            self.current_temp_state = 100
        elif self.current_temp_state < 0:
            self.current_temp_state = 0

        self.current_state = math.ceil(self.current_temp_state/20)

        is_changed = clk_state != self.clk_last_state
        self.clk_last_state = clk_state
        return is_changed
