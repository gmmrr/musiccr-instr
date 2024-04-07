from mfrc522 import MFRC522
import time
import threading


class NFC:
    def __init__(self):

        self.reader = MFRC522()

        self.trailer_block = 11
        self.key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
        self.block_addrs = [8,9,10]

        self.id = None
        self.text = ''


    def wait(self):
        '''

        '''
        while True:
            (status, TagType) = self.reader.Request(self.reader.PICC_REQIDL)
            if status == self.reader.MI_OK:
                break


    def parse(self, uid):
        '''

        '''
        record_1 = []
        record_2 = []
        record_3 = []

        if uid == record_1:
            return 1
        elif uid == record_2:
            return 2
        elif uid == record_3:
            return 3
        else:
            return 1



    def read(self):
        '''
        Read data from NFC tag

        Args:
            None
        Returns:
            data (str): data read from NFC tag
        '''

        # 0. wait until new nfc detected
        t_wait = threading.Thread(self.wait())
        t_wait.start()
        t_wait.join()

        print('NFC: Read')


        # 1. define status
        (status, TagType) = self.reader.Request(self.reader.PICC_REQIDL)

        if status != self.reader.MI_OK:
            return None


        # 2. decide id
        (status, uid) = self.reader.Anticoll()
        if status != self.reader.MI_OK:
            return None

        # 3. make sure there are no multiple nfc detected
        self.reader.SelectTag(uid)
        status = self.reader.Authenticate(
            self.reader.PICC_AUTHENT1A, self.trailer_block , self.key, uid)

        # 4. change id to accessible one
        self.id = self.parse(uid)

        # 5. get text (or message) inside
        if status == self.reader.MI_OK:
            data = []
            for block_num in self.block_addrs:
                block = self.reader.ReadTag(block_num)
                if block:
                    data += block
            if data:
                self.text = ''.join(chr(i) for i in data)

        # 6. reset
        time.sleep(0.5)
        self.reader.StopAuth()
        self.e_nfc_detect.clear()

        return self.id
