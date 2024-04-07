import threading
import RPi.GPIO as GPIO
import time


# ------------------------------
# import components
# ------------------------------
from component import knob
from component import slider
from component import nfc
from api import music
from component import button


# ------------------------------
# init variables
# ------------------------------
is_working = False

e_bpm_update = threading.Event()
e_pitch_update = threading.Event()
e_volume_update = threading.Event()
e_track_update = threading.Event()

val_bpm = 3
val_pitch = 3
val_volume = 50
val_track = 1

pdspeaker = music.PDSpeaker()



# ------------------------------
# init pins
# ------------------------------
pin_bpm_knob_clk = 36
pin_bpm_knob_dt = 38
pin_volume_knob_clk = 8
pin_volume_knob_dt = 10



# ------------------------------
# define threads
# ------------------------------
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


def nfc_thread():
    '''

    '''
    global is_working
    global e_track_update
    global val_track


    nfc_obj = nfc.NFC()


    while True:
        while is_working:

            val_track, text = nfc_obj.read()

            if val_track:
                print(f'NFC_id: {val_track}')
                print(f'NFC_msg: {text}')
            else:
                print("No NFC detected")

            e_track_update.set()



def pdspeaker_thread():
    '''

    '''

    global is_working
    global e_bpm_update
    global e_pitch_update
    global e_volume_update
    global pdspeaker


    c_pdspeaker_update = threading.Condition()


    while True:
        while is_working:

            with c_pdspeaker_update:
                c_pdspeaker_update.wait_for(lambda:
                    e_bpm_update.is_set()     or  e_pitch_update.is_set()  or  # Option 1 and 2
                    e_volume_update.is_set()  or  e_track_update.is_set()  )   # Option 3 and 4


                # Option 1. Update BPM
                if e_bpm_update.is_set():
                    pdspeaker.send_bpm(val_bpm)
                    e_bpm_update.clear()


                # Option 2. Update Pitch
                if e_pitch_update.is_set():
                    pdspeaker.send_pitch(val_pitch)
                    e_pitch_update.clear()


                # Option 3. Update Volume
                if e_volume_update.is_set():
                    pdspeaker.send_volume(val_volume)
                    e_volume_update.clear()


                # Option 4. Update Track
                if e_track_update.is_set():
                    pdspeaker.send_track(val_track)
                    e_track_update.clear()


def playbutton_thread():
    '''

    '''

    global is_working
    global pdspeaker


    play_button = button.Button(pin = 40)


    while True:

        play_button.wait()
        is_working = not is_working






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
    t_bpm_knob = threading.Thread(target=bpm_knob_thread)
    t_pitch_slider = threading.Thread(target=pitch_slider_thread)
    t_volume_knob = threading.Thread(target=volume_knob_thread)
    t_nfc = threading.Thread(target=nfc_thread)
    t_pdspeaker = threading.Thread(target=pdspeaker_thread)
    t_playbutton = threading.Thread(target=playbutton_thread)

    # Step 2: Start Threads
    t_bpm_knob.start()
    t_pitch_slider.start()
    t_volume_knob.start()
    t_nfc.start()
    t_pdspeaker.start()
    t_playbutton.start()

    # Step 3: Wait for Threads to Finish
    t_bpm_knob.join()
    t_pitch_slider.join()
    t_volume_knob.join()
    t_nfc.join()
    t_pdspeaker.join()
    t_playbutton.join()

    # Step 4: Finish
    GPIO.cleanup()

    print("Instrument: End")



if __name__ == "__main__":
    try:
        time.sleep(3)
        main()
    except:
        KeyboardInterrupt
