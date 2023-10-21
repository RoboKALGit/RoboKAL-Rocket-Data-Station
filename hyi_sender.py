import numpy as np
import struct

import serial



def to_bytes(value):
    if isinstance(value,int):
        return bytearray(struct.pack("I",value))
    elif isinstance(value,float):
        return bytearray(struct.pack("f",value))
    

def check_sum(arr: np.ndarray):
    return arr[4:75].sum() % 256



def convert_hyi_format(values,packet_count):
    data = np.ndarray(shape=(78,),dtype=np.uint8)

    data[:] = np.zeros(data.shape)

    data[0:4] = 0xFF, 0xFF, 0x54, 0x52

    data[4] = 0 #TAKIM ID
    data[5] = packet_count #PAKET SAYAÇ

    data[6:10] = to_bytes(values["altitude"]) #İRTİFA

    data[10:14] = to_bytes(values["rocket_gps_altitude"]) #ROKET GPS İRTİFA
    data[14:18] = to_bytes(values["rocket_lat"]) #ROKET ENLEM
    data[18:22] = to_bytes(values["rocket_lng"]) #ROKET BOYLAM

    data[22:26] = to_bytes(values["load_gps_altitude"]) #GÖREV YÜKÜ GPS İRTİFA
    data[26:30] = to_bytes(values["load_lat"]) #GÖREV YÜKÜ ENLEM
    data[30:34] = to_bytes(values["load_lng"]) #GÖREV YÜKÜ BOYLAM

    data[34:38] = to_bytes(0.00) #KADEME GPS İRTİFA
    data[38:42] = to_bytes(0.00) #KADEME GPS ENLEM
    data[42:46] = to_bytes(0.00) #KADEME GPS BOYLAM

    data[46:50] = to_bytes(values["gyro_x"]) #JİROSKOP X
    data[50:54] = to_bytes(values["gyro_y"]) #JİROSKOP Y
    data[54:58] = to_bytes(values["gyro_z"]) #JİROSKOP Z

    data[58:62] = to_bytes(values["accel_x"]) #İVME X
    data[62:66] = to_bytes(values["accel_y"]) #İVME Y
    data[66:70] = to_bytes(values["accel_z"]) #İVME Z

    data[70:74] = to_bytes(abs(values["angle_z"])) #AÇI 

    data[74] = 4 if data["state"] else 1 #DURUM

    data[75] = check_sum(data) #CHECK SUM

    data[76:78] = 0x0D, 0x0A

    return data.tobytes()


class Sender:
    
    def __init__(self,port,baud_rate):
        self._serial = serial.Serial(port,baud_rate)
        self.packet_count = 0
    
    def send(self,data):
        self._serial.write(convert_hyi_format(data,self.packet_count))
        self.packet_count = ( self.packet_count + 1 ) % 256




