import RPi.GPIO as GPIO
import time
import subprocess
import multiprocessing


from component import nfc


def nfc_read_thread(queue):
    '''

    '''
    nfc_obj = nfc.NFC()

    nfc_obj.update()

    val_track, _ = nfc_obj.get_id()

    val = queue.get()
    val['val'] = val_track
    queue.put(val)


def main():

    print("Instrument: Start")
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    #################

    val_track = 1
    last_val_track = 1


    cmd = "aplay src/sea.wav&"
    subprocess.call([cmd], shell=True)


    while True:

        # Step 1: Get NFC ID
        queue = multiprocessing.Queue()
        queue.put({'val': val_track})

        t_read = multiprocessing.Process(target=nfc_read_thread, args=(queue, ))
        t_read.start()
        t_read.join(3)  # timesout = 3 seconds

        val_track = queue.get()['val']
        if val_track == None:
            val_track = last_val_track


        # Step 2: Play the track
        if val_track != last_val_track:
            print(val_track, last_val_track)
            if val_track == 1:
                cmd = "aplay src/sea.wav&"
            elif val_track == 2:
                cmd = "aplay src/city.wav&"
            else:
                cmd = "aplay src/forest.wav&"

            subprocess.call (["pkill aplay"], shell=True)
            subprocess.call([cmd], shell=True)

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
