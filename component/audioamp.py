import RPi.GPIO as GPIO
from api import music
import time
import pygame


class AudioAmp():
    def __init__(self, music):
        self.music = music

        pygame.mixer.init()
        pygame.mixer.music.set_volume(0.5)

        self.is_updating = False


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
        time.sleep(0.1)

        self.is_updating = True


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
        while True:
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                if self.is_updating:
                    break
                else:
                    continue
            break

        self.is_updating = False


    def stop(self):
        '''

        '''
        pygame.mixer.music.stop()
