class Slider():
    def __init__(self):
        self.value = 0
        self.min = 0
        self.max = 100
        self.step = 1
        self.orientation = 'horizontal'
        self.size_hint = (None, None)
        self.width = 100
        self.height = 50
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

    def on_value(self):
        pass

class PitchSlider():
    def __init__(self):
        # derive from Slider class
        super().__init__()


class BPMSlider():
    def __init__(self):
        # derive from Slider class
        super().__init__()