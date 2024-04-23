from DIPPID import SensorUDP
from time import sleep
# INFO: see demo_hearbeat.py

# use UPD (via WiFi) for communication
PORT = 5700
sensor = SensorUDP(PORT)

while(True):
    print("caps", sensor.get_capabilities())

    if(sensor.has_capability('accelerometer')):
        print("acc", sensor.get_value('accelerometer'))
        # acc_x = float(sensor.get_value('accelerometer')['x'])
        # print(acc_x)
    
    if(sensor.has_capability('button_1')):
        print("b_1", sensor.get_value('button_1'))

    sleep(1)

# def handle_data(data):
#     print(data)
#     # print("data", sensor.get_value('accelerometer'))
#     # print(float(sensor.get_value('accelerometer')['x']))
#     # print(data)

# sensor.register_callback('data', handle_data)
