class Music():
    def __init__(self):
        self.reset()


    def reset(self):
        print("Music:Reset")
        self.music = None
        self.music_order = []
        self.music_section = []


    # decode
    def decode_btdata_to_music(self):
        print("Music:Decode BT to music")

    def decode_nfcdata_to_order(self):
        print("Music:Decode NFC to order")

    def decode_music_to_section(self):
        print("Music:Decode music into sections")


    # receive music from bt, and receive order from nfc, and save them in section form
    def update(self):
        '''
        update music by receiving data from updated bt and nfc

        Args:
        - bt
        - nfc

        Returns:
        -
        '''
        print("Music:Update")

        # self.music = self.decode_btdata_to_music(self.bt.get_data())
        # self.music_order = self.decode_nfcdata_to_order(self.nfc.get_data())
        # self.msuic_section = self.decode_music_to_section(self.music, self.music_order)


    def get_music_section(self):
        print("Music:Get music_section (send to Speaker)")