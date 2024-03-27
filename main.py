from tornado import httpclient
from client import Client
from arduino import Arduino
from lidar import Lidar
import json
from tornado.ioloop import IOLoop, PeriodicCallback

IP = "10.53.1.73"
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
        lidar.start()

        #Serial communication to Arduino
        arduino = Arduino()
        arduino.start()

        #Websocket communication to server
        request = httpclient.HTTPRequest(f"ws://{IP}:{PORT}/agv", headers=header)
        client = Client(request, 5)
        def clientOnMsg(msg):
            if msg is None:
                return
            data = {
                "cmd": msg
            }
            print("Sending: ", data)
            arduino.send(json.dumps(data))
        client.connect(clientOnMsg)

        def sendAGVState():
            data = {
                "container": arduino.getContainer(),
                "collision": arduino.getCollision(),
                "orientation": arduino.getOrientation(),
                "acceleration": arduino.getAcceleration(),
                "power": arduino.getPower(),
                "lidar": lidar.getScanData()
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