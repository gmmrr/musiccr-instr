# from mfrc522 import SimpleMFRC522
#
# reader = SimpleMFRC522()
#
# print("test")
#
# id, text = reader.read()
# print("test")
# print(f"ID: {id}")
# print(f"Text: {text}")

import time
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import pygame

GPIO.setmode(GPIO.BCM) #changed to BCM because that's what SimpleMFRC522 is in... I think?

#setup pins for the maglocks
GPIO.setup(2, GPIO.OUT) #these pins keep getting errors? Not sure if there are overlaps here?
GPIO.setup(3, GPIO.OUT)

#the following GPIO setup is for 4 different buttons.
GPIO.setup(23, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(17, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(24, GPIO.IN, GPIO.PUD_UP) #changed from 22 to 24 because of an issue with pins being referenced in MFR522 code.
#we didn't use any sort of resistor and allowed for the raspberry pi to control the voltage of these buttons.

reader = SimpleMFRC522()

#Turning on Maglocks
GPIO.output(2, GPIO.HIGH)
GPIO.output(3, GPIO.HIGH)
