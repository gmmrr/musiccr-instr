from machine import Pin

class AudioAmp():
    def __init__(self, pin, music, volume_knob, light):
        self.pin = Pin(pin, Pin.OUT)

        self.music = music

        self.volume_knob = volume_knob
        self.light = light

    def play(self):
        self.pin.on()
        print("Speaker:play")

    def stop(self):
        self.pin.off()
        print("Speaker:stop")