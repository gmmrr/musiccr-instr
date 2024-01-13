class Light():
    def __init__(self, pin):
        self.pin = pin

    def reset(self):
        pass

    def turn_on(self):
        self.state = True

    def turn_off(self):
        self.state = False
