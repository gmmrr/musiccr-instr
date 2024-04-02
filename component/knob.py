class Knob():
    def __init__(self, pin):
        self.pin = pin


class VolumeKnob(Knob):
    def __init__(self, pin):
        # derive from Slider class
        super().__init__(pin)

    def update(self):
        print("VolumeKnob:Update")

class BPMKnob(Knob):
    def __init__(self, pin):
        # derive from Slider class
        super().__init__(pin)

    def update(self):
        print("BPMKnob:Update")
