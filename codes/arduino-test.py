
# import serial
# from time import sleep
# arduino = serial.Serial(port='COM8', baudrate=115200, timeout=.1)

# # print(arduino)

# slaveAdd = 0
# CommandAdd = 0
# data1 = 0
# data2 = 10
# datalength = 0
# test_type = 5

# def writeString(x):
#     x=str(x)
#     arduino.write(bytes(x, 'utf-8'))
#     print(bytes(x, 'utf-8'))
#     sleep(0.05)


# # arduino.WriteString (test_type & "," & slaveAdd & "," & CommandAdd & "," & datalength & "," & data1 & "," & data2)


# writeString(test_type)
# writeString(slaveAdd)
# writeString(CommandAdd)
# writeString(datalength)
# writeString(data1)
# writeString(data2)





import serial
import time
import sys


arduino = serial.Serial(port='COM8', baudrate=115200, timeout=.1)


# arduino.write('500005.00')
# time.sleep(0.05)
# data = arduino.readline()
# print(data)


def write_read(x):
	print(x)
	arduino.write(x)
	time.sleep(1)
	data = arduino.read()
	return data


while True:
    num = input("Enter a number: ")
    value = write_read(num)
    print(value)



input()

try:
	from pyfirmata import Arduino, util
	import pyfirmata
	from time import sleep
	import sys
except:
	import pip
	pip.main(['install','pyfirmata'])
	from pyfirmata import Arduino, util
	import pyfirmata




from pyfirmata import Arduino, util
import pyfirmata
from time import sleep, time
import sys

print('Initializing Arduino...')
board = pyfirmata.Arduino('COM8')
print('Arduino initialization complete.')

iterator = util.Iterator(board)
iterator.start()

# a = board.get_pin('a:0:i')
# print(a.read())
RELAY = board.get_pin('d:11:o')

RELAY.write(0)

while True:
	# x = input("On the relay (y or n)?: ")
	# if x == 'y':
	# 	RELAY.write(1)
	# elif x == 'n':
	# 	RELAY.write(0)
	# else: print("Invalid input. Enter y or n.")

	RELAY.write(1)
	sleep(1)
	RELAY.write(0)
	sleep(1)
# while True:
#     board.digital[13].write(1)
#     sleep(.5)
#     board.digital[13].write(0)
#     sleep(.5)



