class Slider():
    def __init__(self, pin):
        self.pin = pin

class PitchSlider(Slider):
    def __init__(self, pin):
        # derive from Slider class
        super().__init__(pin)

    def update(self):
        print("PitchSlider:Update")