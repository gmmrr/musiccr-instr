from machine import Pin
from api import music
from component import knob, light

class AudioAmp():
    def __init__(self, pin):
        self.pin = Pin(pin, Pin.OUT)


    def play(self, music):
        '''
        Args:
        - light: to turn it on
        - volume_knob: to set the volume as expectation

        Returns:
        - void
        '''
        print("Speaker:Play")


    def stop(self):
        '''
        Args:
        - light: to turn it off
        '''
        print("Speaker:Stop")


    def update(self, music):
        '''
        Args:
        - music: to update the music

        Returns:
        - void
        '''
        print("Speaker:UpdateMusic")
        # music
