from tornado import httpclient
from client import Client
from arduino import Arduino
from lidar import Lidar
import json
from tornado.ioloop import IOLoop, PeriodicCallback

IP = "localhost"
PORT = 8080
header = { 
        'websocketpass':'1234', 
        'id':'1'
    }
ioloop = IOLoop.instance()

if __name__ == "__main__":
    try:
        #Start Lidar
        lidar = Lidar()
        lidar.init()
        lidar.start()

        #Serial communication to Arduino
        arduino = Arduino("COM8")
        arduino.start()

        #Websocket communication to server
        request = httpclient.HTTPRequest(f"ws://{IP}:{PORT}/agv", headers=header)
        client = Client(request, 5)
        def clientOnMsg(msg):
            if msg is None:
                return
            print(msg)
            arduino.send(msg)
        client.connect(clientOnMsg)

        def sendAGVState():
            data = {
                "container": arduino.getContainer(),
                "collision": arduino.getCollision(),
                "orientation": arduino.getOrientation(),
                "acceleration": arduino.getAcceleration(),
                "power": arduino.getPower()
                # "lidar": lidar.getScanData()
            }
            client.send(json.dumps(data))
        PeriodicCallback(sendAGVState, 1000).start()
        ioloop.start()
    except KeyboardInterrupt:
        ioloop.stop()
        client.closeConnection()
        arduino.close()
        lidar.stop()
        print("Exit")
    except Exception as e:
        print("error catched")
        ioloop.stop()
        client.closeConnection()
        arduino.close()
        lidar.stop()
        print("Exit")