from machine import Pin
from utime import sleep

# import instrument components
from component import bluetooth, nfc
from data import music
from component import knob, slider, light, audioamp

# define instrument components
bt = bluetooth.Bluetooth()
nfc = nfc.NFC()

music = music.Music()

volume_knob = knob.Knob(pin = -1)
pitch_slider = slider.PitchSlider(pin = -1)
bpm_slider = slider.BPMSlider(pin = -1)
light = light.Light(pin = -1)
speaker = audioamp.AudioAmp(pin = 0, music=music, volume_knob=volume_knob, light=light)

pico_led = Pin("LED", Pin.OUT)

# define files
music = "music.mp3"


# main function
try:
    print("Instrument:Start")
    while True:

        pico_led.on()
        speaker.play()

        sleep(10)

        pico_led.off()
        speaker.stop()

        sleep(1)


except KeyboardInterrupt:
    pass
finally:
    pico_led.off()
    speaker.stop()
    print("Instrument:Finish")


