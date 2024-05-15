import RPi.GPIO as GPIO
import time
import subprocess

from component import nfc

def main():

    print("Instrument: Start")
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    #################

    val_track = 1
    last_val_track = val_track

    nfc_obj = nfc.NFC()


    while True:

        # Step 1: Get NFC ID
        nfc_obj.update()
        val_track, _ = nfc_obj.get_id()
        if val_track == None:  # if no card is detected, then set it as previous one
            val_track = last_val_track

        # Step 2: Play the track
        if val_track != last_val_track:
            if val_track == 1:
                file_path = "src/sea.wav"
            elif val_track == 2:
                file_path = "src/city.wav"
            else:
                file_path = "src/forest.wav"

            subprocess.run(['aplay', file_path])

        # Step 3: Update last value
        last_val_track = val_track


    #################
    GPIO.cleanup()
    print("Instrument: End")



if __name__ == "__main__":
    try:
        time.sleep(3)
        main()
    except:
        KeyboardInterrupt
