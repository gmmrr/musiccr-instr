# from mfrc522 import SimpleMFRC522
#
# reader = SimpleMFRC522()
#
# print("test")
#
# text = "Hello, world"
# id, text_written = reader.write(text)
# print("test")
# print(f"ID: {id}")
# print(f"Text Written: {text_written}")
#
# id, text = reader.read()
# print("test")
# print(f"ID: {id}")
# print(f"Text: {text}")

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

try:
        text = input('New data:')
        print("Now place your tag to write")
        reader.write(text)
        print("Written")

finally:
        GPIO.cleanup()
