from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

print("test")

id, text = reader.read()
print("test")
print(f"ID: {id}")
print(f"Text: {text}")
