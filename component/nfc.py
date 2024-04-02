from api import MFRC522
import signal

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    print("Ctrl+C captured, ending read.")

class NFC:
    def __init__(self, pin):
        self.pin = pin
        self.MIFAREReader = MFRC522.MFRC522()
        signal.signal(signal.SIGINT, end_read)

    def read(self):
        '''
        Read data from NFC tag

        Args:
            None
        Returns:
            data (str): data read from NFC tag
        '''
        # return self.nfc_reader.read()
        #!/usr/bin/env python
        # Scan for cards
        (status,TagType) = self.MIFAREReader.MFRC522_Request(self.MIFAREReader.PICC_REQIDL)

        # If a card is found
        if status == self.MIFAREReader.MI_OK:
            print("Card detected")

        # Get the UID of the card
        (status,uid) = self.MIFAREReader.MFRC522_Anticoll()

        # If we have the UID, continue
        if status == self.MIFAREReader.MI_OK:

            # print(UID
            print("Card read UID: %s,%s,%s,%s" % (uid[0], uid[1], uid[2], uid[3]))
