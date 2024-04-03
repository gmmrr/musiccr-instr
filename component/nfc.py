from mfrc522 import MFRC522

class NFC:
    def __init__(self):

        self.reader = MFRC522()

        self.trailer_block = 11
        self.key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
        self.block_addrs = [8,9,10]

        self.id = None
        self.text = ''


    def read(self):
        '''
        Read data from NFC tag

        Args:
            None
        Returns:
            data (str): data read from NFC tag
        '''

        print('NFC: Read')
        (status, TagType) = self.reader.Request(self.reader.PICC_REQIDL)

        if status != self.reader.MI_OK:
            return None, None

        (status, uid) = self.reader.Anticoll()
        if status != self.reader.MI_OK:
            return None, None
        self.id = uid

        self.reader.SelectTag(uid)
        status = self.reader.Authenticate(
            self.reader.PICC_AUTHENT1A, self.trailer_block , self.key, uid)

        if status == self.reader.MI_OK:
            data = []
            for block_num in self.block_addrs:
                block = self.reader.ReadTag(block_num)
                if block:
                    data += block
            if data:
                self.text = ''.join(chr(i) for i in data)

        self.reader.StopAuth()

        return self.id, self.text
