import RPi.GPIO as GPIO
import math
import threading

class Knob():
    def __init__(self, clk_pin, dt_pin):
        self.clk_pin = clk_pin
        self.dt_pin = dt_pin

        self.current_state = 50

        self.e_rotate = threading.Event()

        GPIO.setup(self.clk_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.dt_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(self.clk_pin, GPIO.BOTH, callback=self.event_callback, bouncetime=50)

    def event_callback(self, _):
        self.e_rotate.set()

    def get_state(self):
        return self.current_state

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
