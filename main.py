import threading
import RPi.GPIO as GPIO
import time

# from mfrc522 import SimpleMFRC522
from pirc522 import RFID
import signal



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

    # reader = SimpleMFRC522()


    try:

        rdr = RFID()
        util = rdr.util()
# Set util debug to true - it will print what's going on
        util.debug = True

        while True:
            # Wait for tag
            rdr.wait_for_tag()

            # Request tag
            (error, data) = rdr.request()
            if not error:
                print("\nDetected")

                (error, uid) = rdr.anticoll()
                if not error:
                    # Print UID
                    print("Card read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3]))

                    # Set tag as used in util. This will call RFID.select_tag(uid)
                    util.set_tag(uid)
                    # Save authorization info (key B) to util. It doesn't call RFID.card_auth(), that's called when needed
                    util.auth(rdr.auth_b, [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])
                    # Print contents of block 4 in format "S1B0: [contents in decimal]". RFID.card_auth() will be called now
                    util.read_out(4)
                    # Print it again - now auth won't be called, because it doesn't have to be
                    util.read_out(4)
                    # Print contents of different block - S1B2 - RFID.card_auth() will be called again
                    util.read_out(6)
                    # We can change authorization info if you have different key in other sector
                    util.auth(rdr.auth_a, [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])
                    #If you want to use methods from RFID itself, you can use this for authorization
                    # This will authorize for block 1 of sector 2 -> block 9
                    # This is once more called only if it's not already authorized for this block
                    util.do_auth(util.block_addr(2, 1))
                    # Now we can do some "lower-level" stuff with block 9
                    rdr.write(9, [0x01, 0x23, 0x45, 0x67, 0x89, 0x98, 0x76, 0x54, 0x32, 0x10, 0x69, 0x27, 0x46, 0x66, 0x66, 0x64])
                    # We can rewrite specific bytes in block using this method. None means "don't change this byte"
                    # Note that this won't do authorization, because we've already called do_auth for block 9
                    util.rewrite(9, [None, None, 0xAB, 0xCD, 0xEF])
                    # This will write S2B1: [0x01, 0x23, 0xAB, 0xCD, 0xEF, 0x98, 0x76......] because we've rewritten third, fourth and fifth byte
                    util.read_out(9)
                    # Let's see what do we have in whole tag
                    util.dump()
                    # We must stop crypto
                    util.deauth()

# rdr.wait_for_tag()
# uid = rdr.read_id(as_number = True)
# if uid is not None:
#     print(f'UID: {uid:X}')

    except KeyboardInterrupt:
        rdr.cleanup()


# ------------------------------
# main
# ------------------------------
def main():

    print("Instrument: Start")

    # Step 0: Initialize
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

    read_rfid()




if __name__ == "__main__":
    time.sleep(10)
    main()
