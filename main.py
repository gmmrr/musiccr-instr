import threading
import RPi.GPIO as GPIO
import time


# ------------------------------
# import components
# ------------------------------
from component import knob
from component import slider
from component import nfc
from component import button
from api import music



# ------------------------------
# init variables
# ------------------------------
e_bpm_update = threading.Event()
e_pitch_update = threading.Event()
e_volume_update = threading.Event()
e_track_update = threading.Event()
e_button_update = threading.Event()

val_bpm = 50
val_pitch = 50
val_volume = 50
val_track = 1
val_pause = 1  # 0 means stop and 1 means play

# pin_bpm_knob_clk = 36
# pin_bpm_knob_dt = 38
# pin_volume_knob_clk = 8
# pin_volume_knob_dt = 10
# pin_nfc = 40



# ------------------------------
# define threads
# ------------------------------
def bpm_knob_thread():
    '''
    Detect the value of BPM knob

    Args:
    - e_bpm_update (threading.Event): event to notify the update of BPM value
    - val_bpm (int): value of BPM
    - bpm_knob (Knob): object of Knob class

    Returns:
    - e_bpm_update (threading.Event): set
    - val_bpm (int)
    '''
    global e_bpm_update
    global val_bpm

    bpm_knob = knob.Knob(clk_pin = 36, dt_pin = 38)

    while True:

        bpm_knob.update()

        print(f"BPM: {bpm_knob.get_state()}")
        val_bpm = bpm_knob.get_state()
        e_bpm_update.set()


def pitch_slider_thread():
    '''
    Detect the value of Pitch slider

    Args:
    - e_pitch_update (threading.Event): event to notify the update of Pitch value
    - val_pitch (int): value of Pitch
    - pitch_slider (Slider): object of Slider class

    Returns:
    - e_pitch_update (threading.Event): set
    - val_pitch (int)
    '''
    global e_pitch_update
    global val_pitch

    pitch_slider = slider.Slider()

    while True:

        if pitch_slider.update():
            print(f"Pitch: {pitch_slider.get_state()}")
            e_pitch_update.set()
            val_pitch = pitch_slider.get_state()


def volume_knob_thread():
    '''
    Detect the value of Volume knob

    Args:
    - e_volume_update (threading.Event): event to notify the update of Volume value
    - val_volume (int): value of Volume
    - volume_knob (Knob): object of Knob class

    Returns:
    - e_volume_update (threading.Event): set
    - val_volume (int)
    '''
    global e_volume_update
    global val_volume

    volume_knob = knob.Knob(clk_pin = 8, dt_pin = 10)

    while True:

        volume_knob.update()

        print(f"Volume: {volume_knob.get_state()}")
        val_volume = volume_knob.get_state()
        e_volume_update.set()


def nfc_thread():
    '''
    Detect the value of NFC tag

    Args:
    - e_track_update (threading.Event): event to notify the update of Track value
    - val_track (int): value of Track
    - nfc_obj (NFC): object of NFC class

    Returns:
    - e_track_update (threading.Event): set
    - val_track (int)
    '''
    global e_track_update
    global val_track

    nfc_obj = nfc.NFC()

    while True:

        val_track = nfc_obj.read()

        print(f'NFC_id: {val_track}')
        e_track_update.set()


def playbutton_thread():
    '''
    Detect if the Play button is pressed

    Args:
    - e_button_update (threading.Event): event to notify the update of Pause value
    - val_pause (int): value of Pause, actually only 0(for stop) and 1(for play)
    - play_button (Button): object of Button class

    Returns:
    - e_button_update (threading.Event): set
    - val_pause (int)
    '''
    global e_button_update
    global val_pause

    play_button = button.Button(pin = 40)

    while True:

        play_button.wait()
        val_pause = not val_pause
        e_button_update.set()


def pdspeaker_thread():
    '''
    Update the value of BPM, Pitch, Volume, Track, and Pause to Pure Data

    Args:
    - e_bpm_update (threading.Event)
    - e_pitch_update
    - e_volume_update
    - e_track_update
    - e_button_update

    - val_bpm      (int)
    - val_pitch
    - val_volume
    - val_track
    - val_pause

    Returns:
    - None
    '''
    global e_bpm_update
    global e_pitch_update
    global e_volume_update
    global e_track_update
    global e_button_update
    global val_bpm
    global val_pitch
    global val_volume
    global val_track
    global val_pause

    pdspeaker = music.PDSpeaker()
    c_pdspeaker_update = threading.Condition()

    while True:

        with c_pdspeaker_update:
            c_pdspeaker_update.wait_for(lambda:
                e_bpm_update.is_set()     or  e_pitch_update.is_set()  or  # Option 1 and 2
                e_volume_update.is_set()  or  e_track_update.is_set()  or  # Option 3 and 4
                e_button_update.is_set()  )                                # Option 5


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


            # Option 5. Update Pause
            if e_button_update.is_set():
                pdspeaker.send_pause(val_pause)
                e_button_update.clear()



# ------------------------------
# main
# ------------------------------
def main():

    print("Instrument: Start")

    # Step 0: Initialize
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)


    # Step 1: Create Threads
    t_bpm_knob = threading.Thread(target=bpm_knob_thread)
    t_pitch_slider = threading.Thread(target=pitch_slider_thread)
    t_volume_knob = threading.Thread(target=volume_knob_thread)
    t_nfc = threading.Thread(target=nfc_thread)
    t_playbutton = threading.Thread(target=playbutton_thread)
    t_pdspeaker = threading.Thread(target=pdspeaker_thread)

    # Step 2: Start Threads
    t_bpm_knob.start()
    t_pitch_slider.start()
    t_volume_knob.start()
    t_nfc.start()
    t_playbutton.start()
    t_pdspeaker.start()

    # Step 3: Wait for Threads to Finish
    t_bpm_knob.join()
    t_pitch_slider.join()
    t_volume_knob.join()
    t_nfc.join()
    t_playbutton.join()
    t_pdspeaker.join()

    # Step 4: Finish
    GPIO.cleanup()

    print("Instrument: End")


if __name__ == "__main__":
    try:
        time.sleep(3)
        main()
    except:
        KeyboardInterrupt
