
from time import sleep
import serial
import threading
import json

class Arduino:
    def __init__(self, port = '/dev/ttyUSB1', baudrate = 9600):
        self.port = port
        self.baudrate = baudrate
        self.ser = None
        #init variable
        self.container = False
        self.collision = False
        self.orientation = {
            "yaw": 0,
            "roll": 0,
            "pitch": 0
        }
        self.acceleration = {
            "x": 0,
            "y": 0,
            "z": 0,
        }
        self.power = 100
    
    def connect(self):
        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=1)
            print("Arduino connected")
        except serial.SerialException as e:
            print("Arduino failed to connect")
            sleep(5)

    def start(self):
        self.runThread = True
        self.thread_read = threading.Thread(target=self.reader, daemon=True)
        self.thread_read.start()
    
    def reader(self):
        while True:
            if self.ser is None:
                self.connect()
                continue
            if not self.runThread:
                break
            buffer = ''
            if not (self.ser.in_waiting > 0):
                continue
            try:
                buffer = self.ser.readline().decode("utf-8")
                print(buffer)
                data = json.loads(buffer)
                self.container = data['container']
                self.collision = data['collision']
                self.orientation = data['orientation']
                self.acceleration = data['acceleration']
                self.power = data['power']
                # print('container: ', self.container, ' collision: ', self.collision,' orientation: ', self.orientation,' acceleration: ', self.acceleration, ' power: ', self.power)
            except Exception as e:
                print('Arduino Error: ', e)

    def send(self, message):
        self.ser.write(bytes(message, 'utf-8'))

    def close(self):
        self.runThread = False
        self.thread_read.join()
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