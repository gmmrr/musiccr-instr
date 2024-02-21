import RPi.GPIO as GPIO
import time
import math

# Function
def section(num):
    if num >= 0:
        return math.floor(num)
    else:
        return math.ceil(num)

# Main Function
class Knob():
    def __init__(self, clk_pin, dt_pin):
        GPIO.setup(clk_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(dt_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        self.reset()

    def reset(self):
        self.deadzone = 4

        self.counter = 0
        self.idle_time = 0

        self.clk_last_state = GPIO.input(self.clk_pin) # in units of the number(counter)
        self.current_state = 3 # in units of 1 to 5, and 3 is default
        self.last_changing_point = 0



    def get_state(self):
        return self.current_state


class VolumeKnob(Knob):
    def __init__(self, clk_pin, dt_pin):
        # derive from Slider class
        super().__init__(clk_pin, dt_pin)
        self.deadzone = 1
        self.current_state = 50

    def update(self):
        clk_state = GPIO.input(self.clk_pin)
        dt_state = GPIO.input(self.dt_pin)

        if clk_state != self.clk_last_state:
            self.idle_time = 0 # start to change
            if dt_state != clk_state:
                self.counter += 1
            else:
                self.counter -= 1

        else: # deal with the idle time
            self.idle_time += 1
            if self.idle_time == 300:
                self.counter = 0
                self.last_changing_point = 0


        if section(self.counter/self.deadzone) > self.last_changing_point:
            if self.current_state < 100:
                self.current_state += 1
            self.last_changing_point = section(self.counter/self.deadzone)
        elif section(self.counter/self.deadzone) < self.last_changing_point:
            if self.current_state > 0:
                self.current_state -= 1
            self.last_changing_point = section(self.counter/self.deadzone)

        if self.idle_time < 300:
            print(self.current_state)


        self.clk_last_state = self.clk_state
        time.sleep(0.01)




class BPMKnob(Knob):
    def __init__(self, clk_pin, dt_pin):
        # derive from Slider class
        super().__init__(clk_pin, dt_pin)
        self.deadzone = 4
        self.current_state = 3

    def update(self):
        clk_state = GPIO.input(self.clk_pin)
        dt_state = GPIO.input(self.dt_pin)

        if clk_state != self.clk_last_state:
            self.idle_time = 0 # start to change
            if dt_state != clk_state:
                self.counter += 1
            else:
                self.counter -= 1

        else: # deal with the idle time
            self.idle_time += 1
            if self.idle_time == 300:
                self.counter = 0
                self.last_changing_point = 0


        if section(self.counter/self.deadzone) > self.last_changing_point:
            if self.current_state < 5:
                self.current_state += 1
            self.last_changing_point = section(self.counter/self.deadzone)
        elif section(self.counter/self.deadzone) < self.last_changing_point:
            if self.current_state > 1:
                self.current_state -= 1
            self.last_changing_point = section(self.counter/self.deadzone)

        if self.idle_time < 300:
            print(self.current_state)


        self.clk_last_state = self.clk_state
        time.sleep(0.01)
