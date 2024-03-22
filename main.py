from tornado import httpclient
from client import Client
from serialCommunication import SerialCommunication
from lidar import Lidar

IP = "127.0.0.1"
PORT = 8080
header = { 
        'websocketpass':'1234', 
        'id':'1'
    }

if __name__ == "__main__":
    #Start Lidar
    # lidar = Lidar("COM7")
    # lidar.init()
    # lidar.start()
    #Serial communication to Arduino
    serial = SerialCommunication()
    serial.start()
    #Websocket communication to server
    request = httpclient.HTTPRequest(f"ws://{IP}:{PORT}/agv", headers=header)
    client = Client(request, 5)
    client.start()