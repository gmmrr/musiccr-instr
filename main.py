import threading
import RPi.GPIO as GPIO
import time

from component import audioamp
from component import knob
from component import light
from component import slider
from api import music

# from component import bluetooth
# from component import nfc

is_working = False
is_volume_updated = False
is_bpm_updated = False
is_pitch_updated = False
is_music_updated = False

val_volume = 50
val_bpm = 3
val_pitch = 3
val_music = "src/s3m3.mp3"




def volume_knob_thread():
    '''

    '''
    global is_working
    global is_volume_updated
    global val_volume

    volume_knob = knob.VolumeKnob(clk_pin = 8, dt_pin = 10)

    while True:
        while is_working:

            if volume_knob.update():
                print(f"Volume: {volume_knob.get_state()}")
                is_volume_updated = True
                val_volume = volume_knob.get_state()


def bpm_knob_thread():
    '''

    '''
    global is_working
    global is_bpm_updated
    global val_bpm

    bpm_knob = knob.BPMKnob(clk_pin = 16, dt_pin = 18)

    while True:
        while is_working:

            if bpm_knob.update():
                print(f"BPM: {bpm_knob.get_state()}")
                is_bpm_updated = True
                val_bpm = bpm_knob.get_state()


# def pitch_slider_thread():
#     '''
#
#     '''
#     global is_working
#     global is_pitch_updated
#     global val_pitch
#
#     pitch_slider = slider.PitchSlider(pin = -1)
#
#     while is_working:
#         if pitch_slider.update():
#             is_pitch_updated = True
#             val_pitch = pitch_slider.get_state()


def music_thread():
    '''

    '''
    global is_working
    global is_music_updated
    global is_bpm_updated
    global is_pitch_updated
    global val_music
    global val_bpm
    global val_pitch

    music_obj = music.Music()

    while True:
        while is_working:

            if is_bpm_updated or is_pitch_updated:

                val_music = music_obj.update(bpm=val_bpm, pitch=val_pitch)
                time.sleep(0.01)

                is_music_updated = True
                is_bpm_updated = False
                is_pitch_updated = False



def speaker_thread():
    '''

    '''
    global is_working
    global is_music_updated
    global is_volume_updated
    global val_music
    global val_volume

    speaker = audioamp.AudioAmp(music=val_music)

    speaker.update(val_music)
    speaker.play()

    while True:
        while is_working:

            if is_music_updated:
                speaker.update(val_music)
                is_music_updated = False

            if is_volume_updated:
                print("!")
                speaker.set_volume(val_volume/100)
                is_volume_updated = False

        speaker.stop()




# def light_thread():
#     '''
#
#     '''
#
#     global is_working
#     light_left = light.Light(pin = -1)
#     light_right = light.Light(pin = -1)
#
#     light_left.turn_on()
#     light_right.turn_on()


def play_button_thread():
    '''

    '''
    global is_working

    while True:

        key = input()
        if key == ' ':
            is_working = not is_working
            print("PlayButton: Start" if is_working else "PlayButton: Stop")








def main():
    GPIO.setmode(GPIO.BOARD)

    print("Instrument: Start")


    # Step 0: Initialize
    global is_working
    is_working = True

    # Step 1: Create Threads
    t_volume_knob = threading.Thread(target=volume_knob_thread)
    t_bpm_knob = threading.Thread(target=bpm_knob_thread)
    # t_pitch_slider = threading.Thread(target=pitch_slider_thread)
    t_music = threading.Thread(target=music_thread)
    t_speaker = threading.Thread(target=speaker_thread)
    # t_light = threading.Thread(target=light_thread)  # actually it just turns on the light once
    t_play_button = threading.Thread(target=play_button_thread)

    # Step 2: Start Threads
    t_volume_knob.start()
    t_bpm_knob.start()
    # t_pitch_slider.start()
    t_music.start()
    t_speaker.start()
    # t_light.start()
    t_play_button.start()

    # Step 3: Wait for Threads to Finish
    t_volume_knob.join()
    t_bpm_knob.join()
    # t_pitch_slider.join()
    t_music.join()
    t_speaker.join()
    # t_light.join()
    t_play_button.join()

    print("Instrument: End")


if __name__ == "__main__":
    main()
