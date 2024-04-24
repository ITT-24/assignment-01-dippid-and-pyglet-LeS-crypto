from DIPPID import SensorUDP
from time import sleep

# use UPD (via WiFi) for communication
PORT = 5700
sensor = SensorUDP(PORT)

while(True):
    print("caps", sensor.get_capabilities())

    if(sensor.has_capability('accelerometer')):
        print("acc", sensor.get_value('accelerometer'))
    
    if(sensor.has_capability('button_1')):
        print("b_1", sensor.get_value('button_1'))

    sleep(1)
