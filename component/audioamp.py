from machine import Pin
from api import music
from component import knob, light

class AudioAmp():
    def __init__(self, pin, music, volume_knob, light):
        self.pin = Pin(pin, Pin.OUT)

        self.music = music

        self.volume_knob = volume_knob
        self.light = light


    def play(self, music):
        '''
        Args:
        - light: to turn it on
        - volume_knob: to set the volume as expectation

        Returns:
        - void
        '''
        print("Speaker:Play")
        # self.pin.on()
        self.light.turn_on()
        # music


    def stop(self):
        '''
        Args:
        - light: to turn it off
        '''
        print("Speaker:Stop")
        # self.pin.off()
        self.light.turn_off()


    def update_music(self, music):
        '''
        Args:
        - music: to update the music

        Returns:
        - void
        '''
        print("Speaker:UpdateMusic")
        # music

    def update_volume(self, volume):
        '''
        Args:
        - volume_knob: to update the volume

        Returns:
        - void
        '''
        print("Speaker:UpdateVolume")
        # volume_knob
