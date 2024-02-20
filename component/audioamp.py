import RPi.GPIO as GPIO
from api import music

import pygame


class AudioAmp():
    def __init__(self, music):
        self.music = music
        self.volume = 0.5
        self.reset()


    def reset(self):
        pygame.mixer.init()
        pygame.mixer.music.set_volume(self.volume)



    def update(self, music):
        '''
        Args:
        - music (string): to update the music

        Returns:
        - void
        '''
        self.music = music
        pygame.mixer.music.load(self.music)
        print(f"Music Playing: {music}")


    def set_volume(self, volume):
        '''

        '''
        self.volume = volume
        print(f"Speaker: SetVolume {self.volume}")
        pygame.mixer.music.set_volume(self.volume)



    def play(self):
        '''
        play the music
        Args:
        -
        Returns:
        - void
        '''
        # pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue

    def stop(self):
        pygame.mixer.music.stop()



# the volume
# pygame.mixer.music.set_volume(0.5)
