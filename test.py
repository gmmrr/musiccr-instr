import struct
import socket

# define the IP address of the Pure Data server
PD_IP = '127.0.0.1'
port_filename = 9000
port_speed = 9001
port_freq = 9002
port_volume = 9003

val_filename = "test.wav"
val_speed = 30
val_freq = 50
val_volume = 50

# val_filename_bytes = val_filename.encode('utf-8')
val_speed_bytes = struct.pack('B', val_speed)
val_freq_bytes = struct.pack('B', val_freq)
val_volume_bytes = struct.pack('B', val_volume)

# socket_filename = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_freq = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_speed = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_volume = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # socket_filename.connect((PD_IP, port_filename))
    socket_speed.connect((PD_IP, port_speed))
    socket_freq.connect((PD_IP, port_freq))
    socket_volume.connect((PD_IP, port_volume))

    # socket_filename.sendall(val_filename_bytes)
    socket_speed.sendall(val_speed_bytes)
    socket_freq.sendall(val_freq_bytes)
    socket_volume.sendall(val_volume_bytes)

    print("Success")

except ConnectionRefusedError:
    print("Fail")

finally:
    # socket_filename.close()
    socket_speed.close()
    socket_freq.close()
    socket_volume.close()
