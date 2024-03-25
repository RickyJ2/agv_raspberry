import serial
import threading
import json

class Arduino:
    def __init__(self, port = '/dev/ttyUSB1', baudrate = 9600):
        self.port = port
        self.baudrate = baudrate
        self.ser = serial.Serial(port, baudrate, timeout=1)
        #init variable
        self.container = False
        self.collision = False
        self.orientation = {0,0,0}
        self.acceleration = {0,0,0}
        self.power = 100

    def start(self):
        self.thread_read = threading.Thread(target=self.reader)
        self.thread_read.start()
    
    def reader(self):
        while True:
            buffer = ''
            buffer = self.ser.readline(self.ser.inWaiting())
            if buffer != '':
                try:
                    data = json.loads(buffer)
                    self.container = data['container']
                    self.collision = data['collision']
                    self.orientation = data['orientation']
                    self.acceleration = data['acceleration']
                    self.power = data['power']
                    print('container: ', self.container)
                    print('collision: ', self.collision)
                    print('orientation: ', self.orientation)
                    print('acceleration: ', self.acceleration)
                    print('power: ', self.power)
                except:
                    print('Error: ', buffer)

    def send(self, message):
        self.ser.write(bytes(message, 'utf-8'))

    def close(self):
        self.ser.close()

    def getContainer(self):
        return self.container
    
    def getCollision(self):
        return self.collision
    
    def getOrientation(self):
        return self.orientation

    def getAcceleration(self):
        return self.acceleration
    
    def getPower(self):
        return self.power