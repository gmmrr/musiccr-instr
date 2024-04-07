from mfrc522 import MFRC522
import time


class NFC:
    def __init__(self):

        self.trailer_block = 11
        self.key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
        self.block_addrs = [8,9,10]

        self.id = None
        self.uid = None
        self.text = ''  # it is not used actually



    def parse(self, uid):
        '''
        Parse the detected id into recorded id

        Args:
        - record_1 (int): recorded id
        - record_2 (int)
        - record_3 (int)

        Returns:
        - parsed id (int)
        '''
        record_1 = [136, 29, 240, 238, 139]
        record_2 = [136, 29, 239, 238, 148]
        record_3 = [136, 29, 238, 238, 149]

        if uid == record_1:
            return 1
        elif uid == record_2:
            return 2
        elif uid == record_3:
            return 3
        else:
            return 1


    def get_id(self):
        '''
        Get the current id of the NFC tag
        Returns:
        - id (int): current id of the NFC tag
        '''
        return self.id, self.uid


    def update(self):
        '''
        Read data from NFC tag

        Returns:
        - self.id (int): parsed id
        '''

        reader = MFRC522()

        # 1. define status
        (status, _) = reader.Request(reader.PICC_REQIDL)
        if status != reader.MI_OK:
            return 1, None

        # 2. decide id
        (status, uid) = reader.Anticoll()
        if status != reader.MI_OK:
            return 1, None

        # 3. make sure there are no multiple nfc detected
        # reader.SelectTag(uid)
        # status = reader.Authenticate(reader.PICC_AUTHENT1A, self.trailer_block, self.key, uid)
        # if status != reader.MI_OK:
        #     return
        # print("3")

        # 4. change id to accessible one
        self.id = self.parse(uid)
        self.uid = uid

        # # 5. get text (or message) inside
        # if status == reader.MI_OK:
        #     data = []
        #     for block_num in self.block_addrs:
        #         block = reader.ReadTag(block_num)
        #         if block:
        #             data += block
        #     if data:
        #         self.text = ''.join(chr(i) for i in data)  # it is not uesd actually

        # 6. reset
        time.sleep(0.5)
        reader.StopAuth()
