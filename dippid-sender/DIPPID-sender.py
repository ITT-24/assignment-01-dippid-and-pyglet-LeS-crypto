import socket
import time 
import numpy as np
import json
from datetime import datetime

IP = '127.0.0.1'
PORT = 5700

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

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
        return super()._simulate_data(data)
    
    def _simulate_axis(self, axis:str):
        """sine functions with diff. frequencies"""
        frequencies = {"x": 37, "y": 501, "z": 1250}

        rand = np.random.randint(100)
        if rand < 70: # simulate rest
            now = datetime.now().minute 
        else: now = datetime.now().second

        sine = np.sin(now * frequencies[axis])
        return sine


class Button(Capabilities):
    def __init__(self, name='button_1'):
        self.name = name
        super().__init__(name=name)
    
    def _simulate_data(self):
        rand = np.random.randint(100)
        click = 0 # button released
        if rand > 50: 
            click = 1  # button pressed
        return super()._simulate_data(data=click)


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

    sock.sendto(sim_data.encode(), (IP, PORT))

    counter += 1
    time.sleep(1)

"""
data-syntax:
message = '{"accelerometer": {"x": "0"} }' # works
message = '{"accelerometer": {"x": "0", "y": "0", "z": "0"} }' # works
i.e:
{ 'accelerometer' : {
    'x': {...},
    'y': {...},
    },
    'button_1' : {
        "
    }
}
"""