from machine import Pin
from utime import sleep
import _thread

# import instrument components
from component import bluetooth, nfc
from api import music
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

# define threads
def test_thread():
    try:
        while True:
            pico_led.on()
            print("LED:ON")

    except KeyboardInterrupt:
        pass
    finally:
        pico_led.off

def speaker_thread():
    try:
        speaker.play()
        while True:
            music.receive_music()
            volume_knob.update()
            speaker.update()

    except KeyboardInterrupt:
        pass
    finally:
        speaker.stop()

def slider_thread():
    try:
        while True:
            pitch_slider.update()
            bpm_slider.update()

    except KeyboardInterrupt:
        pass
    finally:
        pass


# start threads
print("Instrument:Start")
_thread.start_new_thread(test_thread, ())
_thread.start_new_thread(speaker_thread, ())
_thread.start_new_thread(slider_thread, ())
print("Instrument:Finish")
