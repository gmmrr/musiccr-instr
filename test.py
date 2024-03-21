import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

print("test")

text = "Hello, world"

try:

    reader.write(text)
    print(f"Written")

    id, text = reader.read()
    print("test")
    print(id)
    print(text)

finally:
    GPIO.cleanup()
