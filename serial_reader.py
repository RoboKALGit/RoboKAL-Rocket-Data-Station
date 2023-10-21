import serial




class Serial:

    def __init__(self,port,baud_rate):
        self._serial = serial.Serial(port,baud_rate)
        self._serial.readline()
    
    def read(self):
        return self._serial.readline().split(";")[0].split(",")