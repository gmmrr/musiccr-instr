import RPi.GPIO as GPIO
from api import music

import pygame


class AudioAmp():
    def __init__(self, music):
        self.music = music
        self.reset()


    def reset(self):
        pygame.mixer.init()
        pygame.mixer.music.set_volume(0.5)



    def update(self, music):
        '''
        Args:
        - music (string): to update the music

        Returns:
        - void
        '''
        self.music = music
        print(f"Music Playing: {music}")
        pygame.mixer.music.load(self.music)


    def set_volume(self, volume):
        '''

        '''
        pygame.mixer.music.set_volume(volume)



    def play(self):
        '''
        play the music

        Args:
        -

        Returns:
        - void
        '''
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue

    def stop(self):
        pygame.mixer.music.stop()



# the volume
# pygame.mixer.music.set_volume(0.5)
