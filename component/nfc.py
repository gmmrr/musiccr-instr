class NFC:
    def __init__(self, pin):
        self.pin = pin

    def read(self):
        '''
        Read data from NFC tag

        Args:
            None
        Returns:
            data (str): data read from NFC tag
        '''
        # return self.nfc_reader.read()

    def write(self, data):
        '''
        Write data to NFC tag

        Args:
            data (str): data to write to NFC tag
        Returns:
            None
        '''
