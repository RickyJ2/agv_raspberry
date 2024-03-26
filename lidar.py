from time import sleep
import math
from adafruit_rplidar import RPLidar, RPLidarException
import threading

class Lidar:
    def __init__(self, port = "/dev/ttyUSB0"):
        self.port = port
        self.scan_data = [0] * 360
        self.lidar = None
        #in mm
        self.max_distance = 10000
        self.min_distance = 0
    
    def checkHealth(self):
        if self.lidar.health[1] == 0 : 
            return True
        else :
            return False

    def connect(self):
        try:
            self.lidar = RPLidar(None, self.port, timeout=3)
            self.lidar.clear_input()
        except RPLidarException as e:
            print(e)
            sleep(5)
        
    def start(self):
        self.runThread = True
        thread = threading.Thread(target=self._scan, daemon=True)
        thread.start()

    def _scan(self):
        while True:
            if self.lidar is None:
                self.connect()
                continue
            if not self.runThread:
                break
            try:
                scan = next(self.lidar.iter_scans())
                temp = [0]*360
                for _, angle, distance in scan:
                    if distance > self.max_distance or distance < self.min_distance:
                        continue
                    temp[min([359, math.floor(angle)])] = distance
                self.scan_data = temp
            except:
                print("Lidar error")
    def getScanData(self):
        return self.scan_data

    def stop(self):
        try:
            self.lidar.stop()
            self.lidar.disconnect()
        except RPLidarException as e:
            print(e)