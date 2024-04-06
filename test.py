import struct
import socket

# convert the value to bytes
def val_to_bytes (val):
    if isinstance(val, int):
        return struct.pack('B', val)
    elif isinstance(val, str):
        if val == "sea.wav":
            return struct.pack('B', 1)
        elif val == "city.wav":
            return struct.pack('B', 2)
        elif val == "forest.wav":
            return struct.pack('B', 3)
        else:
            return struct.pack('B', 1)
    else:
        return struct.pack('B', val)


# define the IP address of the Pure Data server
PD_IP = '127.0.0.1'
port_filename = 9000
port_speed = 9001
port_freq = 9002
port_volume = 9003
port_pause = 9004

# build the socket
socket_filename = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_speed = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_freq = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_volume = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_pause = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# make built socket to connect to the Pure Data server
socket_filename.connect((PD_IP, port_filename))
socket_speed.connect((PD_IP, port_speed))
socket_freq.connect((PD_IP, port_freq))
socket_volume.connect((PD_IP, port_volume))
socket_pause.connect((PD_IP, port_pause))

# assume the value
val_filename = "sea.wav"
val_speed = 50
val_freq = 50
val_volume = 50
val_pause = 1


try:
    # send the value to the Pure Data server
    socket_filename.sendall(val_to_bytes(val_filename))
    socket_speed.sendall(val_to_bytes(val_speed))
    socket_freq.sendall(val_to_bytes(val_freq))
    socket_volume.sendall(val_to_bytes(val_volume))
    socket_pause.sendall(val_to_bytes(val_pause))

    print("Success")


except ConnectionRefusedError:
    print("Fail")

finally:
    socket_filename.close()
    socket_speed.close()
    socket_freq.close()
    socket_volume.close()
    socket_pause.close()
