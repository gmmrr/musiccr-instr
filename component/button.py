import RPi.GPIO as GPIO

class Button:
    def __init__(self, pin):
        self.pin = pin

        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


    def wait(self):
        '''
        '''
        while True:
            if GPIO.input(self.pin) == GPIO.HIGH:
                break
