class Slider():
    def __init__(self, pin):
        self.pin = pin
        self.state = 3

    def get_state(self):
        return self.state

class PitchSlider(Slider):
    def __init__(self, pin):
        # derive from Slider class
        super().__init__(pin)

    def update(self):
        print("PitchSlider:Update")