class Music():
    def __init__(self):
        self.reset()


    def reset(self):
        print("Music:Reset")


    # receive music from bt, and receive order from nfc, and save them in section form
    def update(self, bpm, pitch):
        '''
        update music by receiving data from updated bt and nfc

        Args:
        - bt
        - nfc

        Returns:
        -
        '''
        print("Music:Update")