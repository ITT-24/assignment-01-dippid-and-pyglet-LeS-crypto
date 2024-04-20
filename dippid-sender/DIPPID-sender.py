import socket
import time 
import numpy as np
import json

IP = '127.0.0.1'
PORT = 5700

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# TODO: simulate input device by sending to a DIPPID receiver via UDP to localhost
    # min. two capabilities: accelerometer, button_1
    # Implement plausible behaviour for simulated sensors
        # e.g. sine functions with diff frequencies for each axis of acc

# ----- PARENT ----- #
class Capabilities:
    def __init__(self, name:str):
        self.data = self._simulate_data()

    def _simulate_data(self, data=None):
        """Abstract class to override"""
        return data

# ----- child-classes ----- #
class Accelerometer(Capabilities):
    def __init__(self, name="accelerometer"):
        self.name=name
        super().__init__(name=name)

    def _simulate_data(self) -> str:
        data = {
                "x": self._simulate_axis(axis="x"),
                "y": self._simulate_axis(axis="y"),
                "z": self._simulate_axis(axis="z"),
                }
        # data = json.dumps(data) # works
        return super()._simulate_data(data)
    
    def _simulate_axis(self, axis:str) -> str:
        # TODO
        axis_data = "0"
        return axis_data


class Button(Capabilities):
    def __init__(self, name='button_1'):
        self.name = name
        super().__init__(name=name)
    
    def _simulate_data(self, data=None):
        # data = {self.name: "clicked"}
        data = "clicked"
        # data = json.dumps(data)
        return super()._simulate_data(data)


def create_simulated_data() -> str:
    acc = Accelerometer() 
    btn_1 = Button()
    
    data = { 
        acc.name: acc.data, 
        btn_1.name: btn_1.data
    } 

    return json.dumps(data)

# ----- SEND-LOOP ----- #

counter = 0

while True:
    
    sim_data = create_simulated_data()
    print("sim_data", sim_data)
    
    # message = '{"accelerometer": {"x": "0"} }' # works
    # message = '{"accelerometer": {"x": "0", "y": "0", "z": "0"} }' # works
    # print("nnot_sim", message)

    sock.sendto(sim_data.encode(), (IP, PORT))

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