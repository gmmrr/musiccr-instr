import threading
import RPi.GPIO as GPIO
import time

from mfrc522 import SimpleMFRC522


# ------------------------------
# import components
# ------------------------------
from component import audioamp
from component import knob
from component import light
from component import slider
from component import playbutton
from api import music

# from component import bluetooth
from component import nfc


# ------------------------------
# init variables
# ------------------------------
is_working = False
is_volume_updated = False
is_bpm_updated = False
is_pitch_updated = False
is_music_updated = False

val_volume = 50
val_bpm = 3
val_pitch = 3
val_music = "src/s3m3.mp3"


# ------------------------------
# init pins
# ------------------------------
# pin_volume_knob_clk = 8
# pin_volume_knob_dt = 10
# pin_bpm_knob_clk = 36
# pin_bpm_knob_dt = 38
# pin_led = 10
# pin_playbutton = 11




# ------------------------------
# define threads
# ------------------------------
def volume_knob_thread():
    '''
    Control the volume knob

    Args:
    - volume_knob: knob.VolumeKnob

    '''
    global is_working
    global is_volume_updated
    global val_volume
    global pin_volume_knob_clk
    global pin_volume_knob_dt

    volume_knob = knob.VolumeKnob(clk_pin = pin_volume_knob_clk, dt_pin = pin_volume_knob_dt)


    while True:
        while is_working:

            if volume_knob.update():
                print(f"Volume: {volume_knob.get_state()}")
                is_volume_updated = True
                val_volume = volume_knob.get_state()


def bpm_knob_thread():
    '''
    Control the BPM knob

    Args:
    - bpm_knob: knob.BPMKnob

    '''
    global is_working
    global is_bpm_updated
    global val_bpm
    global pin_bpm_knob_clk
    global pin_bpm_knob_dt

    bpm_knob = knob.BPMKnob(clk_pin = pin_bpm_knob_clk, dt_pin = pin_bpm_knob_dt)

    while True:
        while is_working:

            if bpm_knob.update():
                print(f"BPM: {bpm_knob.get_state()}")
                is_bpm_updated = True
                val_bpm = bpm_knob.get_state()


def pitch_slider_thread():
    '''
    Control the pitch slider

    Args:
    - pitch_slider: slider.PitchSlider

    '''
    global is_working
    global is_pitch_updated
    global val_pitch

    pitch_slider = slider.PitchSlider()

    while True:
        while is_working:

            if pitch_slider.update():
                print(f"Pitch: {pitch_slider.get_state()}")
                is_pitch_updated = True
                val_pitch = pitch_slider.get_state()


def music_thread():
    '''
    To change the music

    Args:
    - Music: api.Music

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
                time.sleep(0.05)

                is_music_updated = True
                is_bpm_updated = False
                is_pitch_updated = False


def speaker_thread():
    '''
    To make the speaker play the music

    Args:
    -

    '''
    global is_working
    global is_music_updated
    global is_volume_updated
    global val_music
    global val_volume

    speaker = audioamp.AudioAmp(music=val_music)

    speaker.update(val_music)

    while True:
        while is_working:

            if is_music_updated:
                speaker.update(val_music)
                time.sleep(0.05)
                is_music_updated = False

                t_speaker_play = threading.Thread(target=speaker.play)
                t_speaker_play.start()

            if is_volume_updated:
                speaker.set_volume(val_volume/100)
                is_volume_updated = False


def light_thread():
    '''
    To deal with the light effect

    '''

    global is_working
    global is_music_updated
    global is_volume_updated
    global val_music
    global val_volume
    global pin_led


    light_obj = light.Light(pin = pin_led)
    light_obj.update(val_music, val_volume)

    # while True:
    #     while is_working:
    #
    #         if is_music_updated or is_volume_updated:
    #             light.update(val_music, val_volume)
    #             time.sleep(0.05)
    #             is_music_updated = False
    #             is_volume_updated = False

    t_light_turn_on = threading.Thread(target=light_obj.turn_on)
    t_light_turn_on.start()

    t_light_turn_on = threading.Thread(target=light_obj.turn_on)
    t_light_turn_on.start()


        # light_obj.turn_off()


def play_button_thread():
    '''

    '''

    global is_working
    global pin_playbutton

    playbutton_obj = playbutton.PlayButton(pin = pin_playbutton)

    while True:
        t_play_button_press = threading.Thread(target=playbutton_obj.wait)
        t_play_button_press.start()

        is_working = not is_working
        print(is_working)


def nfc_thread():
    '''
    '''
    global is_working
    nfc_obj = nfc.NFC()
    while True:
        while is_working:
            nfc_obj.read()
            print("NFC: Detected")
            time.sleep(0.5)



def read_rfid():

    print("test1")

    reader = SimpleMFRC522()

    print("test2")

    # print("Place card to write: ")
    # text = "Hello, world"
    # reader.write(text)
    # print(f"Written.")

    print("test3")

    time.sleep(3)
    print("Place your card to read: ")
    id, text = reader.read()
    print("Read.")
    print(id)
    print(text)

    print("test4")


# ------------------------------
# main
# ------------------------------
def main():

    print("Instrument: Start")

    # Step 0: Initialize
    GPIO.cleanup()
    GPIO.setmode(GPIO.BOARD)
    global is_working
    is_working = True

    # Step 1: Create Threads
    # t_volume_knob = threading.Thread(target=volume_knob_thread)
    # t_bpm_knob = threading.Thread(target=bpm_knob_thread)
    # t_pitch_slider = threading.Thread(target=pitch_slider_thread)
    # t_music = threading.Thread(target=music_thread)
    # t_speaker = threading.Thread(target=speaker_thread)
    # t_light = threading.Thread(target=light_thread)
    # t_play_button = threading.Thread(target=play_button_thread)
    # t_nfc = threading.Thread(target=nfc_thread)

    # Step 2: Start Threads
    # t_volume_knob.start()
    # t_bpm_knob.start()
    # t_pitch_slider.start()
    # t_music.start()
    # t_speaker.start()
    # t_light.start()
    # t_play_button.start()
    # t_nfc.start()

    # Step 3: Wait for Threads to Finish
    # t_volume_knob.join()
    # t_bpm_knob.join()
    # t_pitch_slider.join()
    # t_music.join()
    # t_speaker.join()
    # t_light.join()
    # t_play_button.join()
    # t_nfc.join()

    print("Instrument: End")

    print(GPIO.getmode())

    read_rfid()





if __name__ == "__main__":
    # time.sleep(10)
    main()
