import struct
import socket

# convert the value to bytes

class PDSpeaker:
    def __init__(self):

        # define the IP address of the Pure Data server
        PD_IP = '127.0.0.1'
        port_bpm = 9001
        port_pitch = 9002
        port_volume = 9003
        port_track = 9000
        port_pause = 9004

        # build the socket
        self.socket_bpm = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_pitch = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_volume = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_track = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_pause = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # make built socket to connect to the Pure Data server
        self.socket_bpm.connect((PD_IP, port_bpm))
        self.socket_pitch.connect((PD_IP, port_pitch))
        self.socket_volume.connect((PD_IP, port_volume))
        self.socket_track.connect((PD_IP, port_track))
        self.socket_pause.connect((PD_IP, port_pause))

        # assume the value
        self.val_bpm = 50
        self.val_pitch = 50
        self.val_volume = 50
        self.val_track = 1
        self.val_pause = 1

        # init the value
        self.socket_bpm.sendall(struct.pack('B', self.val_bpm))
        self.socket_pitch.sendall(struct.pack('B', self.val_pitch))
        self.socket_volume.sendall(struct.pack('B', self.val_volume))
        self.socket_track.sendall(struct.pack('B', self.val_track))
        self.socket_pause.sendall(struct.pack('B', self.val_pause))




    def send_bpm(self, val):
        try:
            self.val_bpm = val
            self.socket_bpm.sendall(struct.pack('B', self.val_bpm))
        except ConnectionRefusedError:
            print("PDSpeaker: Connetion Failed")


    def send_pitch(self, val):
        try:
            self.val_pitch = val
            self.socket_pitch.sendall(struct.pack('B', self.val_pitch))
        except ConnectionRefusedError:
            print("PDSpeaker: Connetion Failed")


    def send_volume(self, val):
        try:
            self.val_volume = val
            self.socket_volume.sendall(struct.pack('B', self.val_volume))
        except ConnectionRefusedError:
            print("PDSpeaker: Connetion Failed")


    def send_track(self, val):
        try:
            self.val_track = val
            self.socket_track.sendall(struct.pack('B', self.val_track))
        except ConnectionRefusedError:
            print("PDSpeaker: Connetion Failed")


    def send_pause(self, val):
        try:
            self.val_pause = val
            self.socket_pause.sendall(struct.pack('B', self.val_pause))
        except ConnectionRefusedError:
            print("PDSpeaker: Connetion Failed")
