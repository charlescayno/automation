from time import sleep, time
from powi.equipment import Arduino
import serial.tools.list_ports
import math

class MultiprotocolControl():

    # data sequence is (1:test_type, 2:i2c Address/ DALI Command1, 3:Register address/Command2, 4:data length, 5:Data1 , 6:Data 2)
    # deviceAddress = slaveAdd
    # registerAddress = CommandAdd

    def __init__(self):
        
        # automatic detection of comm port
        ports = serial.tools.list_ports.comports()
        commPort = 'None'
        for i in range(0, len(ports)):
            port = str(ports[i])
            print(port)
            
            if 'Silicon Labs CP210x USB to UART Bridge' in port:
                commPort = port[3]
                print(commPort)

            if 'USB Serial Device' in port:
                commPort = port[3:5]
                print(commPort)
            
        
        if commPort != 'None':
            self.arduino = Arduino(f'{commPort}')
            print(f'Connected to COM{commPort}')
        else:
            print('Connection Issue!')

    def _isfloat(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    def _hex2dec(self, hex='00'):
        return int(hex,16)
    
    def _send_command(self, test_type, slaveAdd, commandAdd, datalength, data1, data2):
        command = f'{test_type},{slaveAdd},{commandAdd},{datalength},{data1},{data2}'
        self.arduino.device.write_raw(command)
    
    """Analog"""

    def manual_set_analog(self, voltage):
        while not self._isfloat(voltage):
            print("Invalid input. ")
            voltage = input('Enter analog voltage (V): ')
        test_type = 5
        slaveAdd = 0
        commandAdd = 0
        datalength = 0
        data1 = 0
        data2 = voltage
        self._send_command(test_type, slaveAdd, commandAdd, datalength, data1, data2)
        sleep(1)
        print(f'{self.arduino.read()} V')
    
    def analog_dimming(self, start, end, step_size):
        while start != end+step_size:
            self.manual_set_analog(start)
            # print(self.arduino.read())
            start += step_size

    """I2C"""

    def manual_set_i2c_cp(self, CP=0, BinnoAddress='00'):
        test_type = 1
        slaveAdd = self._hex2dec(BinnoAddress)
        commandAdd = self._hex2dec('12')
        datalength = 1
        data1 = CP
        data2 = 0
        
        self._send_command(test_type, slaveAdd, commandAdd, datalength, data1, data2)

    def manual_set_i2c_linear_dimming(self, option='logarithmic', BinnoAddress='00'):
        while not option == 'linear' or option == 'logarithmic':
            option = input("Invalid option.")
        if option == 'linear': opt = 1
        if option == 'logarithmic': opt = 0

        test_type = 1
        slaveAdd = self._hex2dec(BinnoAddress)
        commandAdd = self._hex2dec('14')
        datalength = 1
        data1 = opt
        data2 = 0

        print(f"Set to {opt}")
        self._send_command(test_type, slaveAdd, commandAdd, datalength, data1, data2)

    def manual_set_i2c(self, BinnoSend, BinnoAddress='00'):

        test_type = 1
        slaveAdd = self._hex2dec(BinnoAddress)
        commandAdd = self._hex2dec('10')
        datalength = 1
        data1 = BinnoSend
        data2 = 0

        print(f"{BinnoSend} bit sent.")
        self._send_command(test_type, slaveAdd, commandAdd, datalength, data1, data2)
        print(f'{self.arduino.read()}')

    """PWM"""

    def manual_set_pwm(self, pwmFrequency=2000, pwmDuty=100):
        
        test_type = 4
        slaveAdd = 0
        commandAdd = 0
        datalength = 0
        data1 = pwmFrequency
        data2 = pwmDuty

        self._send_command(test_type, slaveAdd, commandAdd, datalength, data1, data2)
        print(f'{self.arduino.read()} Hz')
        print(f'{self.arduino.read()} %')

    """Rheostat"""

    def manual_set_rheostat(self, RheostatValue=100):

        test_type = 6
        slaveAdd = 0
        commandAdd = 0
        datalength = 0
        data1 = 0
        data2 = math.ceil(RheostatValue/100*1023)

        self._send_command(test_type, slaveAdd, commandAdd, datalength, data1, data2)
        print(f'{self.arduino.read()} Ohms')



# control = MultiprotocolControl()
# start = time()


# end = time()
# print(end-start)
