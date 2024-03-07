import serial
import threading
import time

class SerialCommunication:
    def __init__(self, port = 'COM8', baudrate = 9600):
        self.port = port
        self.baudrate = baudrate
        self.ser = serial.Serial(port, baudrate, timeout=1)
        print("Serial communication initialized")
        # time.sleep(2) # wait for the Arduino to initialize

    def start(self):
        self.thread_read = threading.Thread(target=self.reader)
        self.thread_read.start()
    
    def reader(self):
        while True:
            buffer = ''
            buffer = self.ser.readline(self.ser.inWaiting())
            print(buffer)
            time.sleep(5)
			# if buffer:
			# 	for conn in WSHandler.connections:
			# 		conn.write_message(buffer)

    def send(self, message):
        self.ser.write(bytes(message, 'utf-8'))
        print(f"Message sent: {message}")

    def receive(self):
        msg = self.ser.readline()
        print(f"Message received: {msg}")
        return msg

    def close(self):
        self.ser.close()