from DIPPID import SensorUDP
# INFO: see demo_hearbeat.py

# use UPD (via WiFi) for communication
PORT = 5700
sensor = SensorUDP(PORT)

def handle_data(data):
    print(data)

sensor.register_callback('data', handle_data)
