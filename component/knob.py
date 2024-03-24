import RPi.GPIO as GPIO
import time
import math
import threading

#------------------
# Parent Class
#------------------
class Knob():
    def __init__(self, clk_pin, dt_pin):
        self.clk_pin = clk_pin
        self.dt_pin = dt_pin

        self.e_rotate = threading.Event()

        GPIO.setup(self.clk_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.dt_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(self.clk_pin, GPIO.BOTH, callback=self.event_callback, bouncetime=50)

    def event_callback(self, channel):
        self.e_rotate.set()

    def get_state(self):
        return self.current_state



#------------------
# Derived Class
#------------------

class VolumeKnob(Knob):
    def __init__(self, clk_pin, dt_pin):
        super().__init__(clk_pin, dt_pin)

        self.current_state = 50


    def update(self):
        # 0. wait until rotate
        self.e_rotate.wait()

        # 1. get value
        clk_state = GPIO.input(self.clk_pin)
        dt_state = GPIO.input(self.dt_pin)

        # 2. change current_state
        temp_state = self.current_state
        temp_state += 1 if dt_state != clk_state else -1

        # 3. if current_state is not in an expected range
        if temp_state > 100:
            temp_state = 100
        elif temp_state < 0:
            temp_state = 0

        # 4. update current_state
        self.current_state = temp_state


class BPMKnob(Knob):
    def __init__(self, clk_pin, dt_pin):
        super().__init__(clk_pin, dt_pin)

        self.current_state = 3

        self.rotate_range = 20
        self.deadzone = self.rotate_range/5


    def update(self):
        # 0. wait until rotate
        self.e_rotate.wait()

        # 1. get value
        clk_state = GPIO.input(self.clk_pin)
        dt_state = GPIO.input(self.dt_pin)

        # 2. change curremt state
        temp_state = self.current_state
        temp_state += 1 if dt_state != clk_state else -1

        # 3. if current_state is not in expected range
        if temp_state > self.rotate_range:
            temp_state = self.rotate_range
        elif temp_state < 1:
            temp_state = 1

        # 4. update current_state
        self.current_state = math.ceil(temp_state/self.deadzone)
