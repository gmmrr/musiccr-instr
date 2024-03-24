import threading
import RPi.GPIO as GPIO
import time


# ------------------------------
# import components
# ------------------------------
from component import audioamp
from component import knob
from component import slider
from component import playbutton
from api import music
from component import nfc


# ------------------------------
# init variables
# ------------------------------
is_working = False

e_volume_update = threading.Event()
e_bpm_update = threading.Event()
e_pitch_update = threading.Event()
e_music_update = threading.Event()

val_volume = 50
val_bpm = 3
val_pitch = 3
val_music = "src/s3m3.mp3"
val_id = 1


# ------------------------------
# init pins
# ------------------------------
pin_volume_knob_clk = 8
pin_volume_knob_dt = 10
pin_bpm_knob_clk = 36
pin_bpm_knob_dt = 38
pin_playbutton = 11




# ------------------------------
# define threads
# ------------------------------
def volume_knob_thread():
    '''

    '''
    global is_working
    global e_volume_update
    global val_volume
    global pin_volume_knob_clk
    global pin_volume_knob_dt

    volume_knob = knob.VolumeKnob(clk_pin = pin_volume_knob_clk, dt_pin = pin_volume_knob_dt)


    while True:
        while is_working:

            volume_knob.update()

            print(f"Volume: {volume_knob.get_state()}")
            val_volume = volume_knob.get_state()
            e_volume_update.set()


def bpm_knob_thread():
    '''

    '''
    global is_working
    global e_bpm_update
    global val_bpm
    global pin_bpm_knob_clk
    global pin_bpm_knob_dt

    bpm_knob = knob.BPMKnob(clk_pin = pin_bpm_knob_clk, dt_pin = pin_bpm_knob_dt)


    while True:
        while is_working:

            bpm_knob.update()

            print(f"BPM: {bpm_knob.get_state()}")
            val_bpm = bpm_knob.get_state()
            e_bpm_update.set()


def pitch_slider_thread():
    '''

    '''
    global is_working
    global e_pitch_update
    global val_pitch

    pitch_slider = slider.PitchSlider()


    while True:
        while is_working:

            if pitch_slider.update():
                print(f"Pitch: {pitch_slider.get_state()}")
                e_pitch_update.set()
                val_pitch = pitch_slider.get_state()


def music_thread():
    '''

    '''
    global is_working
    global e_music_update
    global e_bpm_update
    global e_pitch_update
    global val_music
    global val_bpm
    global val_pitch
    global val_id

    music_obj = music.Music()
    c_music_update = threading.Condition()


    while True:
        while is_working:

            with c_music_update:
                c_music_update.wait_for(lambda: e_bpm_update.is_set() or e_pitch_update.is_set())

                val_music = music_obj.update(bpm=val_bpm, pitch=val_pitch)

                e_music_update.set()
                e_bpm_update.clear()
                e_pitch_update.clear()


def speaker_thread():
    '''

    '''
    global is_working
    global e_music_update
    global e_volume_update
    global val_music
    global val_volume

    speaker = audioamp.AudioAmp(music=val_music)
    c_speaker_update = threading.Condition()

    speaker.update(val_music)


    while True:
        while is_working:

            with c_speaker_update:
                c_speaker_update.wait_for(lambda: e_music_update.is_set() or e_volume_update.is_set())

                if e_music_update.is_set():
                    speaker.update(val_music)

                    t_speaker_play = threading.Thread(target=speaker.play)
                    t_speaker_play.start()

                    e_music_update.clear()


                if e_volume_update.is_set():
                    speaker.set_volume(val_volume/100)

                    e_volume_update.clear()



def play_button_thread():
    '''

    '''
    global is_working
    global pin_playbutton

    playbutton_obj = playbutton.PlayButton(pin = pin_playbutton)


    while True:

        playbutton_obj.wait()
        is_working = not is_working


def nfc_thread():
    '''

    '''
    global is_working
    global val_id

    nfc_obj = nfc.NFC()


    while True:
        while is_working:

            val_id, text = nfc_obj.read()
            if val_id:
                print(f'NFC_id: {val_id}')
                print(f'NFC_msg: {text}')
            else:
                print("No NFC detected")





# ------------------------------
# main
# ------------------------------
def main():

    print("Instrument: Start")

    # Step 0: Initialize
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)

    global is_working
    is_working = True

    # Step 1: Create Threads
    t_volume_knob = threading.Thread(target=volume_knob_thread)
    t_bpm_knob = threading.Thread(target=bpm_knob_thread)
    t_pitch_slider = threading.Thread(target=pitch_slider_thread)
    t_music = threading.Thread(target=music_thread)
    t_speaker = threading.Thread(target=speaker_thread)
    t_play_button = threading.Thread(target=play_button_thread)
    t_nfc = threading.Thread(target=nfc_thread)

    # Step 2: Start Threads
    t_volume_knob.start()
    t_bpm_knob.start()
    t_pitch_slider.start()
    t_music.start()
    t_speaker.start()
    t_play_button.start()
    t_nfc.start()

    # Step 3: Wait for Threads to Finish
    t_volume_knob.join()
    t_bpm_knob.join()
    t_pitch_slider.join()
    t_music.join()
    t_speaker.join()
    t_play_button.join()
    t_nfc.join()

    # Step 4: Finish
    GPIO.cleanup()

    print("Instrument: End")



if __name__ == "__main__":
    try:
        time.sleep(3)
        main()
    except:
        KeyboardInterrupt
