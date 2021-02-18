# python script showing battery details 
import psutil 
from time import time, sleep
import matplo
# function returning time in hh:mm:ss 
def convertTime(seconds): 
	minutes, seconds = divmod(seconds, 60) 
	hours, minutes = divmod(minutes, 60) 
	return "%d:%02d:%02d" % (hours, minutes, seconds) 

# returns a tuple 
battery = psutil.sensors_battery() 

while (1):
    print("Battery percentage : ", battery.percent) 
    # print("Power plugged in : ", battery.power_plugged) 

    # converting seconds to hh:mm:ss 
    # print("Battery left : ", convertTime(battery.secsleft))
    sleep(1)


print("Battery percentage : ", battery.percent) 
# print("Power plugged in : ", battery.power_plugged) 

# converting seconds to hh:mm:ss 
# print("Battery left : ", convertTime(battery.secsleft))