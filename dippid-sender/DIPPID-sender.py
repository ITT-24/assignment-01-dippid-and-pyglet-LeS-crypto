import socket
import time 
import numpy as np

IP = '127.0.0.1'
PORT = 5700

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# TODO: simulate input device by sending to a DIPPID receiver via UDP to localhost
    # min. two capabilities: accelerometer, button_1
    # Implement plausible behaviour for simulated sensors
        # e.g. sine functions with diff frequencies for each axis of acc

# class Capabilities:
#     def __init__(self, name:str, value:dict):
#         pass
counter = 0
while True:
    
    # "data" = 'data' demo_reciever.py/register_callback
    message = '{"data" : ' + str(counter) + '}'
    print(message)

    sock.sendto(message.encode(), (IP, PORT))

    counter += 1
    time.sleep(1)

# https://robotics.stackexchange.com/q/10233
# https://stackoverflow.com/q/3921467

"""
{ 'accelerometer' : {
    'x': {...},
    'y': {...},
    },
    'button_1' : {
        "
    }
}
"""