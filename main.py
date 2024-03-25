from tornado import httpclient
from client import Client
from arduino import Arduino
from lidar import Lidar
import json

IP = "10.53.8.42"
PORT = 8080
header = { 
        'websocketpass':'1234', 
        'id':'1'
    }

if __name__ == "__main__":
    #Start Lidar
    lidar = Lidar()
    lidar.init()
    lidar.start()
    #Serial communication to Arduino
    arduino = Arduino()
    arduino.start()
    #Websocket communication to server
    request = httpclient.HTTPRequest(f"ws://{IP}:{PORT}/agv", headers=header)
    client = Client(request, 5)
    client.start()
    while(1):
    #send data to server
        data = {
            "container": arduino.getContainer(),
            "collision": arduino.getCollision(),
            "orientation": arduino.getOrientation(),
            "acceleration": arduino.getAcceleration(),
            "power": arduino.getPower(),
            "lidar": lidar.getScanData()
        }
        client.send(json.dumps(data))
        #consume message from server
        if(client.msg.length > 0):
            data = {
                "cmd" : client.msg.pop(0)
            }
            arduino.send(json.dumps(data))