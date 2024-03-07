from tornado import httpclient
from client import Client
from serialCommunication import SerialCommunication


IP = "localhost"
PORT = 8080
header = { 
        'websocketpass':'1234', 
        'id':'1'
    }

if __name__ == "__main__":
    serial = SerialCommunication()
    serial.start()
    request = httpclient.HTTPRequest(f"ws://{IP}:{PORT}/agv", headers=header)
    client = Client(request, 5)
    client.start()