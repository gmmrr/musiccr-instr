import RPi.GPIO as GPIO
from api import music

import time

import pygame


class AudioAmp():
    def __init__(self, music):
        self.music = music
        self.reset()


    def reset(self):
        '''

        '''
        pygame.mixer.init()
        pygame.mixer.music.set_volume(1)


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
        time.sleep(0.05)


    def set_volume(self, volume):
        '''

        '''
        print(volume)
        pygame.mixer.music.set_volume(volume)
        time.sleep(0.05)


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
                continue


    def stop(self):
        '''

        '''
        pygame.mixer.music.stop()
