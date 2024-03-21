
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
