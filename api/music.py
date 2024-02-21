class Music():
    def __init__(self):
        self.reset()



    def reset(self):
        self.bpm = 3
        self.pitch = 3

    # receive music from bt, and receive order from nfc, and save them in section form
    def update(self, bpm, pitch):
        '''
        update music by receiving data from updated bt and nfc

        Args:

        Returns:
        -
        '''

        self.bpm = bpm
        self.pitch = pitch

        return f"@/src/s{self.bpm}m{self.pitch}.mp3"
