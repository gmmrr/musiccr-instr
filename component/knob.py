class Knob():
    def __init__(self, pin):
        self.pin = pin
        self.state = 0

    def update(self):
        pass

    def get_state(self):
        return self.state


class VolumeKnob(Knob):
    def __init__(self, pin):
        # derive from Slider class
        super().__init__(pin)
        self.state = 50

class BPMKnob(Knob):
    def __init__(self, pin):
        # derive from Slider class
        super().__init__(pin)
        self.state = 3



# ------------------------------------------------------------------
from machine import Pin
from time import sleep
import math

clk_pin = Pin(12, Pin.IN, Pin.PULL_DOWN)
dt_pin = Pin(13, Pin.IN, Pin.PULL_DOWN)

def section(num):
    if num >= 0:
        return math.floor(num)
    else:
        return math.ceil(num)

try:
    print("Rotary Encoder:Start")

    deadzone = 4

    counter = 0
    idle_time = 0

    clk_last_state = clk_pin.value() # in units of the number(counter)
    current_state = 3 # in units of 1 to 5, and 3 is default
    last_changing_point = 0

    while True:
        clk_state = clk_pin.value()
        dt_state = dt_pin.value()

        if clk_state != clk_last_state:
            idle_time = 0 # start to change
            if dt_state != clk_state:
                counter += 1
            else:
                counter -= 1

        else: # deal with the idle time
            idle_time += 1
            if idle_time == 300:
                print("Rotary Encoder:Idle")
                counter = 0
                last_changing_point = 0

       
        if section(counter/deadzone) > last_changing_point:
            if current_state < 5:
                current_state += 1
            last_changing_point = section(counter/deadzone)
        elif section(counter/deadzone) < last_changing_point:
            if current_state > 1:
                current_state -= 1
            last_changing_point = section(counter/deadzone)

        if idle_time < 300:
            print(current_state)    
            

        clk_last_state = clk_state
        sleep(0.01)
        
except KeyboardInterrupt:
    print("Rotary Encoder:Stop")
finally:
    pass
