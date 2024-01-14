class Slider():
    def __init__(self, pin):
        self.pin = pin

class PitchSlider():
    def __init__(self):
        # derive from Slider class
        super().__init__()

    def update(self):
        print("PitchSlider:Update")


class BPMSlider():
    def __init__(self):
        # derive from Slider class
        super().__init__()

    def update(self):
        print("BPMSlider:Update")
