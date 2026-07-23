import serial
from time import time, sleep


# import serial.tools.list_ports
# ports = serial.tools.list_ports.comports()

# for i in range(0, len(ports)):
#     port = str(ports[i])
#     print(port)





ser = serial.Serial(port='COM5',baudrate=115200,timeout=1)
print(ser.name)         # check which port was really used
# sleep(2)
ser.write(b'5,0,0,0,0,3')     # write a string
# sleep(1)
print(ser.read())
while True:
    c = ser.read()
    if len(c) == 0:
        break
    # print(c)
    print (int(c.hex(), 16))

# print(int(ser.read_until('\r').hex(),16))

input()
ser.close()             # close port