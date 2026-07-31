
import serial
import time
import sys


piqi = serial.Serial(port='COM6', baudrate=115200, timeout=.1)

data = piqi.read()


# # arduino.write('500005.00')
# # time.sleep(0.05)
# # data = arduino.readline()
# # print(data)


# def write_read(x):
#     print(f"user input: {x}")
#     print(f"user input to byte: {x.encode('utf-8')}")
#     arduino.write(x.encode('utf-8'))
#     time.sleep(1)
#     print()
#     data = arduino.read()
#     print(f"byte received from from arduino: {data}")
#     data_decoded = data.decode("utf-8")
#     print(f"from arduino (byte) to string: {data_decoded}")
#     print(f"type of received: {type(data_decoded)}")
#     print()
#     return data


# while True:
#     num = str(input("Enter a number: "))
#     value = write_read(num)
#     # print(value)



# input()

# try:
# 	from pyfirmata import Arduino, util
# 	import pyfirmata
# 	from time import sleep
# 	import sys
# except:
# 	import pip
# 	pip.main(['install','pyfirmata'])
# 	from pyfirmata import Arduino, util
# 	import pyfirmata




# from pyfirmata import Arduino, util
# import pyfirmata
# from time import sleep, time
# import sys

# print('Initializing Arduino...')
# board = pyfirmata.Arduino('COM8')
# print('Arduino initialization complete.')

# iterator = util.Iterator(board)
# iterator.start()

# # a = board.get_pin('a:0:i')
# # print(a.read())
# RELAY = board.get_pin('d:11:o')

# RELAY.write(0)

# while True:
# 	# x = input("On the relay (y or n)?: ")
# 	# if x == 'y':
# 	# 	RELAY.write(1)
# 	# elif x == 'n':
# 	# 	RELAY.write(0)
# 	# else: print("Invalid input. Enter y or n.")

# 	RELAY.write(1)
# 	sleep(1)
# 	RELAY.write(0)
# 	sleep(1)
# # while True:
# #     board.digital[13].write(1)
# #     sleep(.5)
# #     board.digital[13].write(0)
# #     sleep(.5)
