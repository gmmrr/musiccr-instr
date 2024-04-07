import RPi.GPIO as GPIO

class Knob():
    def __init__(self, clk_pin, dt_pin):
        self.clk_pin = clk_pin
        self.dt_pin = dt_pin

        self.state = 50
        self.clk_last_state = 50

        GPIO.setup(self.clk_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.dt_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        self.index = 0


    def get_state(self):
        '''
        Get the current state of the knob

        Returns:
        - state (int): current state of the knob
        '''
        return self.state


    def update(self):
        '''
        Update the current state of the knob
        '''
        clk_state = GPIO.input(self.clk_pin)
        dt_state = GPIO.input(self.dt_pin)

        if clk_state != self.clk_last_state:
            self.state += 1 if dt_state != clk_state else -1

        if self.state > 100:
            self.state = 100
        elif self.state < 0:
            self.state = 0

        self.clk_last_state = clk_state
