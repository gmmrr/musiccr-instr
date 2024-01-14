from machine import Pin
from utime import sleep

# import instrument components
from component import bluetooth, nfc
from data import music
from component import knob, light, audioamp
from api import slider

# define instrument components
bt = bluetooth.Bluetooth(pin=-1)
nfc = nfc.NFC(pin=-1)

music = music.Music(bt, nfc)

volume_knob = knob.Knob(pin = -1)
pitch_slider = slider.PitchSlider(pin = -1)
bpm_slider = slider.BPMSlider(pin = -1)
light = light.Light(pin = -1)
speaker = audioamp.AudioAmp(pin=0, music=music, volume_knob=volume_knob, light=light)  # speaker should be linked to the light, volume and music

pico_led = Pin("LED", Pin.OUT)

# main function
try:
    print("Instrument:Start")
    while True:  # Keep Instrument working

        is_playing = True
        while is_playing: #
            pico_led.on()
            speaker.play()


        pico_led.off()
        speaker.stop()


except KeyboardInterrupt:
    pass
finally:
    pico_led.off()
    speaker.stop()
    print("Instrument:Finish")
