import RPi.GPIO as GPIO
import time

class PlayButton():
    def __init__(self, pin):
        self.pin = pin

        self.state = True

        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)


    def update(self):
        if GPIO.input(self.pin) == GPIO.LOW:
            self.state = not self.state
            time.sleep(0.2)

        return self.state
