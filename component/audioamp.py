from machine import Pin
from api import music

class AudioAmp():
    def __init__(self, pin, music):
        self.pin = Pin(pin, Pin.OUT)
        self.music = music


    def update(self, music):
        '''
        Args:
        - music: to update the music

        Returns:
        - void
        '''
        self.music = music
