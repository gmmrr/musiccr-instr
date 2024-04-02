import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time

reader = SimpleMFRC522()

print("test")

text = "Hello, world"

try:

    print("Place card to write")
    reader.write(text)
    print(f"Written")


    time.sleep(3)
    print("Now place your tag to read")
    id, text = reader.read()
    print("test")
    print(id)
    print(text)

finally:
    GPIO.cleanup()
