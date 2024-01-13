from machine import Pin

class AudioAmp():
    def __init__(self, pin, music, volume_knob, light):
        self.pin = Pin(pin, Pin.OUT)

        self.music = music

        self.volume_knob = volume_knob
        self.light = light

    def play(self):
        print("Speaker:play")
        self.pin.on()
        self.light.turn_on

    def stop(self):
        print("Speaker:stop")
        self.pin.off()
        self.light.turn_off
