from machine import Pin
import time
import _thread

from component import audioamp
# from component import bluetooth
from component import knob
from component import light
# from component import nfc
from component import slider
from api import music

is_working = True
is_music_updated = False

pitch_slider = slider.PitchSlider(pin = -1)
bpm_knob = knob.BPMKnob(pin = -1)
music= music.Music(pitch_slider = pitch_slider, bpm_knob = bpm_knob)

volume_knob = knob.VolumeKnob(pin = -1)
light = light.Light(pin = -1)
speaker = audioamp.AudioAmp(pin = -1, music = music, volume_knob = volume_knob, light = light)

def music_thread():
    global is_working
    global is_music_updated

    global pitch_slider
    global bpm_knob
    global music

    while is_working:
        if pitch_slider.update() or bpm_knob.update():
            music.update(pitch_slider.get_pitch(), bpm_knob.get_bpm())
            time.sleep(0.2)
            is_music_updated = True


def main():
    global is_working
    global is_music_updated

    global volume_knob
    global light
    global speaker
    global music

    print("Instrument: Start")
    _thread.start_new_thread(music_thread, [])

    try:
        while True:
            speaker.play(music)

            if is_music_updated is True:
                speaker.update_music(music)
                is_music_updated = False

            if volume_knob.update():
                speaker.update_volume(volume_knob.get_volume()


    except KeyboardInterrupt:
        speaker.stop()
        print("Instrument: Finish")

    finally:
        is_working = False
        is_music_updated = False
        time.sleep(0.4)  # wait for the thread to finish


        print("Instrument: Finish")

if __name__ == "__main__":
    main()
