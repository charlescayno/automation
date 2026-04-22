# For controlling the CP2112 interface
from asyncore import write
from dll import SLABHIDtoSMBUS as smbus
from dll.hidsmbus_definitions import HID_SMBUS_DEFINITIONS as HID_SMBUS

# Define PD commands, CCG2 register structures and responses
from pd import pd_types
from pd.pd_types import PD_COMMAND, HPI_V1_REG as CY_PD_REG, HPI_RESPONSE as CY_PD_RESP

# Needed for running PPS requests periodically
from threading import Timer

from enum import Enum

class PAT_TOOL_SETTINGS(Enum):
    PPS_REQUEST_INTERVAL_SEC = 8


class CP2112(smbus.HidSmbusDevice):
    """ USB HID to SMBUS Device Class

        CP2112 is an interface for USB to connect to SMBUS (I2C) devices
        It is used in this program to connect to multiple PD sink controller devices (CCG2)
        This class uses SLABHIDtoSMBUS.dll from Silicon Labs through the wrapper taken from
        Silicon Labs USBXpressHostSdk
        # https://www.silabs.com/documents/public/software/USBXpressHostSDK-Win.zip

        And can be found in the below directory after installing
        # C:/SiliconLabs/USBXpressHostSDK/CP2112/Release/x64
    """
    def __init__(self, *args, **kwargs):
        super().__init__()

        # CP2112 VID and PID defined in datasheet
        self.vid = 0x10C4
        self.pid = 0xEA90

        # Placeholder for PD sink controller objects to be controlled by the SMBUS interface
        self.pd_sink_controllers = []
        
        # Set the I2C multiplexer
        self.i2c_multiplexer = I2C_Multiplexer()
        self.i2c_multiplexer.smbus = self

        # Open the
        self.num_devices = 0

        self.connection_ok = False
        
        self.open()
        if self.num_devices == 1:
            self.connection_ok = True
            self.set_smbus_config()



    ###############################################################################################
    #  Functions using dll wrapper configured for PAT tool use                                    #
    ###############################################################################################

    def get_matching_devices(self):
        self.num_devices = smbus.GetNumDevices()

    def open(self):
        self.num_devices = smbus.GetNumDevices()
        
        if self.num_devices == 0:
            print("No PAT tool detected.")
        
        elif self.num_devices > 1:
            print("More than 1 PAT tool is detected. Please remove the unused device")

        else:
            try:
                self.Open()
                print("PAT tool opened successfully")
            except:
                print("PAT tool is detected but cannot be accessed by this program. Please close other programs that may be accessing this device.")
    

    def set_smbus_config(self):

        address = 0x2
        autoReadRespond = 0
        writeTimeout = 1000
        readTimeout = 1000
        sclLowTimeout = 0
        transferRetries = 1
        bitRate = 100000

        self.SetSmbusConfig(bitRate, address, autoReadRespond, writeTimeout,
                        readTimeout,sclLowTimeout, transferRetries)
    
    # CCG2 device address is 0x08 with 7bit addressing
    def write_request(self, write_buffer, device_addr=0x10):
        self.WriteRequest(device_addr, write_buffer, len(write_buffer))

    
    def read_request(self, slave_address, register_address, num_bytes_to_read, read_buffer):
        """Reads the value of a register

        Keyword arguments:
        @   register_address    --  register address to be read
        @   num_bytes_to_read   --  number of bytes to read
        @   read_buffer         --  variable where to store the read value
        """

        self.address_read_request(slave_address,register_address,num_bytes_to_read)
        self.get_transfer_status()
        self.force_read_response(num_bytes_to_read)
        return self.get_read_response()[:num_bytes_to_read]

    def address_read_request(self, slave_address, register_address, num_bytes_to_read):
        
        # Make sure that the device is Opened
        if self.IsOpened():# == HID_SMBUS.SUCCESS:
            
            # Issue an address read request
            offset = (register_address).to_bytes(length=1, byteorder='big')
            status = self.AddressReadRequest(address=slave_address,
                                            count=num_bytes_to_read,
                                            offset_size=1,
                                            offset=offset)

    def get_transfer_status(self):
        self.TransferStatusRequest()
        status = self.GetTransferStatusResponse()

    def force_read_response(self, num_bytes_to_read):
        if self.IsOpened():
            self.ForceReadResponse(count=num_bytes_to_read)
        
    def get_read_response(self):
        if self.IsOpened():
            read_buffer = self.GetReadResponse()
            read_buffer_list = list(bytes(read_buffer))
            return read_buffer_list
            

    ###############################################################################################
    #  Added functions for interacting with PDSinkController and I2C_Multiplexer classes          #
    ###############################################################################################

    def add_PDController(self, PD_Controller):
        
        # PD controller object can access the SMBUS master
        PD_Controller.smbus = self

        # Add the PD sink controller to the list of PD controllers linked to the SMBUS interface
        self.pd_sink_controllers.append(PD_Controller)

        # Get the multiplexer register value

        PD_Controller.multiplexer_reg = self.i2c_multiplexer.get_i2c_slot_regvalue(PD_Controller.multiplexer_slot)
        


class PDSinkController():
    """ Class for CCG2 Sink Controller device

        The CCG2 sink device is a slave to the SMBUS interface
        We don't know how to change the I2C address of the CCG2 device
        so an I2C multiplexer (TCA9548) is used to address 
        multiple CCG2 units

        TCA9548 Multiplexer has 8 channels that can be selected

        Keyword Arguments:
        multiplexer_slot    --      SCL/SDA channel used by the CCG2 slave device
        
    """
    def __init__(self, multiplexer_slot = 0, is_multiport = False, *args, **kwargs):
        
        # If is_multiport = False, the multiplexer will not be used
        self.is_multiport = is_multiport

        # I2C address is 0x08 by default for CCG2 devices
        self.i2c_address=0x10
        
        # PAT tool can be assigned by using add_PDController from the PAT tool object
        
        # Register value to be used when switching the multiplexer channel 
        # self.multiplexer_reg = I2C_Multiplexer.get_i2c_slot_regvalue(multiplexer_slot)
        self.multiplexer_slot = multiplexer_slot

        # List of all PDOs including Fixed PDO, Augmented PDO
        self.pdo_list = []

        # List of PPS object positions
        self.pps_list = []

        # Thread for running periodic PPS requests
        self.pps_periodic_request_thread = []

        # Flag for checking if PPS request thread is running
        self.pps_request_thread_running = False

        # Flag for checking connection
        self.connection_ok = False


    def fixed_pdo_request(self, object_position, iout):

        FVRDO_buffer = pd_types.FVRDO()
        FVRDO_buffer.bits.object_position = object_position
        FVRDO_buffer.bits.iout_operating = int(iout/10)
        FVRDO_buffer.bits.iout_max = int(iout/10)

        register_write_fullreg = FVRDO_buffer.asbyte

        write_buffer = [0,0,0,0,0]
        write_buffer[0] = CY_PD_REG.CURRENT_RDO.value
        write_buffer[1] = register_write_fullreg & 0xFF
        write_buffer[2] = ( register_write_fullreg >> 8 ) & 0xFF
        write_buffer[3] = ( register_write_fullreg >> 16 ) & 0xFF 
        write_buffer[4] = ( FVRDO_buffer.bits.object_position << 4 ) & 0xFF
        
        if self.is_multiport:
            # Activate multiplexer channel where the PD sink controller is connected to
            self.activate_mux_channel()

        self.smbus.WriteRequest(address=self.i2c_address, buffer=write_buffer, count=len(write_buffer))
    
    def pps_request(self, vout, iout, 
                        object_position = -1,
                        capability_mismatch = 0, 
                        usb_comm_capable = 0, 
                        no_usb_suspend = 0):
        """Send a PPS request

        Keyword arguments:
        vout -- output voltage request in 20mV increments
        iout -- current limit request in 50mA increments
        object_position -- PDO object position
                
        """
        # Prepare PPS request data object buffer
        PPSRDO_buffer = pd_types.PPSRDO()

        # Clear all bit positions
        PPSRDO_buffer.asbyte = 0

        # Object position
        # If object position is not defined, check if there is a PPS object
        # If there is a PPS object, use the PPS object
        if object_position == -1:
            if len(self.pps_list) != 0:
                PPSRDO_buffer.bits.object_position = self.pps_list[0]
        
        # If not, use the input
        else:
            PPSRDO_buffer.bits.object_position = object_position

        # Voltage and Current setting
        PPSRDO_buffer.bits.operating_voltage = int(round ( vout / 0.02))  & 0x7FF
        PPSRDO_buffer.bits.operating_current = int(round ( iout / 0.05)) & 0x7F

        # Other Settings
        PPSRDO_buffer.bits.no_usb_suspend = no_usb_suspend
        PPSRDO_buffer.bits.usb_comm_capable = usb_comm_capable
        PPSRDO_buffer.bits.capability_mismatch = capability_mismatch

        # Prepare write buffer
        write_buffer = [0,0,0,0,0]

        PPSRDO_32bit = PPSRDO_buffer.asbyte

        write_buffer[0] = CY_PD_REG.CURRENT_RDO.value
        write_buffer[1] = PPSRDO_32bit & 0xFF           # 1st byte
        write_buffer[2] = ( PPSRDO_32bit >> 8 ) & 0xFF  # 2nd byte
        write_buffer[3] = ( PPSRDO_32bit >> 16 ) & 0xFF # 3rd byte
        write_buffer[4] = ( PPSRDO_32bit >> 24 ) & 0xFF # 4th byte

        # Store the write buffer in the object so it can be accessed
        # by the periodic request function
        self.pps_write_buffer = write_buffer

        # Write the buffer once in the I2C
        # Let the timed thread do the rest
        self.pps_write()

        # If there is a thread currently running,
        # stop it first so there will not be a buildup of threads
        # with multiple PPS requests
        if self.pps_request_thread_running == True:
            self.pps_periodic_request_thread.stop()
        
        # Create a RepeatedTimer object which will run the pps_periodic_write
        # function with interval defined by the PAT_TOOL_SETTINGS
        self.pps_periodic_request_thread = RepeatedTimer(
            interval=PAT_TOOL_SETTINGS.PPS_REQUEST_INTERVAL_SEC.value,
            function=self.pps_write
        )
        self.pps_request_thread_running = True



    def pps_write(self):
        """Periodically request the PPS RDO defined in the pps_write_buffer
        
        This function is to be called with a RepeatedTimer object
        """
        if self.is_multiport:
            # Activate multiplexer channel where the PD sink controller is connected to
            self.activate_mux_channel()

        # Send an SMBUS write request to the PD controller
        # with the write_buffer as the message
        self.smbus.WriteRequest(address=self.i2c_address, 
                                buffer=self.pps_write_buffer, 
                                count=len(self.pps_write_buffer))


    def get_source_caps(self):
        """ Get the source capability of the power supply
        
        """
        buffer = list()
        self.pdo_list = []
        self.pps_list = []
        if self.is_multiport:
            # Activate multiplexer channel where the PD sink controller is connected to
            self.activate_mux_channel()

        # Get PDO Count
        self.source_pdo_count = self.smbus.read_request(slave_address=self.i2c_address,
                                                        register_address=CY_PD_REG.SRC_PDO_CNT.value,
                                                        num_bytes_to_read=1,
                                                        read_buffer=buffer)[0]

        # Read PDOs
        self.source_caps_received = []
        for index in range(0, self.source_pdo_count):
            source_cap_received = self.smbus.read_request(slave_address=self.i2c_address,
                                            register_address=CY_PD_REG.SRC_PDO.value + 4*index,
                                            num_bytes_to_read=4,
                                            read_buffer=buffer)
            # If only 3 bytes are received, assume 4th byte is 0x00
            if len(source_cap_received) == 3:
                source_cap_received.append(0)
            self.source_caps_received.append(source_cap_received)
            
            # time.sleep(0.05)
        
        # Decode PDOs
        pdo_source_cap = pd_types.PDO()
        fpdo_source_cap = pd_types.FPDOSupply()
        apdo_source_cap = pd_types.PPSAPDO()

        # Loop through source caps, check if FPDO or APDO
        for index, source_cap in enumerate(self.source_caps_received):
            source_cap_uint32 = self.list_to_uint32(source_cap)
            pdo_source_cap.asbyte = source_cap_uint32

            # Process the uint32 data accordingly
            if pdo_source_cap.bits.supply_type == pd_types.PDO_SUPPLY_TYPE.FIXED.value:
                fpdo_source_cap.asbyte = source_cap_uint32

                # Create a PDO Object for the PD Sink Controller
                PDO_buffer = PDO()
                PDO_buffer.voltage = fpdo_source_cap.bits.voltage * pd_types.PD_MULTIPLIER.FPDO_SUPPLY_VOLT_MULTIPLIER.value
                PDO_buffer.max_current = fpdo_source_cap.bits.max_current * pd_types.PD_MULTIPLIER.FPDO_SUPPLY_MAX_CURRENT_MULTIPLIER.value
                PDO_buffer.supply_type = pd_types.PDO_SUPPLY_TYPE.FIXED.value
                PDO_buffer.object_position = index + 1
                PDO_buffer.text = f'PDO {PDO_buffer.object_position}: {PDO_buffer.voltage}mV , {PDO_buffer.max_current} mA'

                self.pdo_list.append(PDO_buffer)

            elif pdo_source_cap.bits.supply_type == pd_types.PDO_SUPPLY_TYPE.AUGMENTED.value:
                apdo_source_cap.asbyte = source_cap_uint32

                # Create a PDO Object for the PD Sink Controller
                PDO_buffer = PDO()
                PDO_buffer.min_voltage = apdo_source_cap.bits.min_voltage * pd_types.PD_MULTIPLIER.PPS_MIN_VOLT_MULTIPLIER.value
                PDO_buffer.max_voltage = apdo_source_cap.bits.max_voltage * pd_types.PD_MULTIPLIER.PPS_MAX_VOLT_MULTIPLIER.value
                PDO_buffer.max_current = apdo_source_cap.bits.max_current * pd_types.PD_MULTIPLIER.PPS_MAX_CURRENT_MULTIPLIER.value
                PDO_buffer.supply_type = pd_types.PDO_SUPPLY_TYPE.AUGMENTED.value
                PDO_buffer.object_position = index + 1
                PDO_buffer.text = f'PDO {PDO_buffer.object_position}: {PDO_buffer.min_voltage}mV' \
                                  f' - {PDO_buffer.max_voltage} mV , {PDO_buffer.max_current} mA'

                self.pdo_list.append(PDO_buffer)
                self.pps_list.append(PDO_buffer.object_position)

        for pdo in self.pdo_list:
            print(pdo.text)

    # Convert the bytes received to a single value and apply Little Endian 
    def list_to_uint32(self, data_list):
        dl = data_list
        return (dl[3]<<24)+(dl[2]<<16)+(dl[1]<<8)+(dl[0])

    # Activate the mux channel associated with the PD Controller object
    def activate_mux_channel(self):

        # disable for normal pat tool
        self.smbus.i2c_multiplexer.activate_channel(self.multiplexer_slot)
    
class I2C_Multiplexer():
    """ Class for the I2C multiplexer using TCA9548
    
        Contains the parameters and methods needed to use the device
    """
    def __init__(self, *args, **kwargs):
        
        # I2C address defined in datasheet is 0x70
        # Somehow each hex digit has to be represented as 5 bits (need confirmation)
        # so 0x70 which is 0b  0111  0000
        # has to become    0b 00111 00000
        # so 0x70 it becomes 0xE0
        self.i2c_address = 0xE4

        # The current channel used is tracked so that the channel switching
        # command is only sent when needed and will not take too much
        # of the SMBUS bandwidth
        self.current_channel = -1

    def get_i2c_slot_regvalue(self, slot):
        """ Generate needed register value to activate the slot
        
            Currently only selecting from pre-generated values
            TCA9548 has 8 selectable I2C channels
            Register has to be set such that the value of the 8bit register
            Corresponds to which channel is connected
            
            For example:
            To select Channel 3 (SC3/SD3)
            
                         7 6 5 4   3 2 1 0
            a value of 0x0 0 0 0   1 0 0 0
            
            or 0x08 must be sent to switch the I2C lines to that channel
        """
        return 2**slot

    def activate_channel(self, channel_number):
        """ Activate the I2C channel selected

            If the channel is already active, the channel change command will not be sent
            to save on SMBUS bandwidth
        """

        # If the channel selected is already active, dont do anything
        if self.current_channel == channel_number:
            return 0

        # If it is not yet active, send a request to the multiplexer I2C address
        # to activate the selected channel
        else:
            self.smbus.WriteRequest(address=self.i2c_address, 
                                    buffer=[self.get_i2c_slot_regvalue(channel_number)], 
                                    count=1)
            self.current_channel = channel_number


class PDO():
    """ Power Data Object for the PD Sink Controller Class
    """

    def __init__(self, *args, **kwargs):
        self.supply_type = None

        # FPDO
        self.voltage = None
        self.max_current = None

        # PPS APDO
        self.min_voltage = None
        self.max_voltage = None

        self.object_position = None
        self.power = None
        self.text = ""



# Code taken from
# https://stackoverflow.com/questions/3393612/run-certain-code-every-n-seconds
# class RepeatedTimer(object):
#     def __init__(self, interval, function, *args, **kwargs):
#         self._timer     = None
#         self.interval   = interval
#         self.function   = function
#         self.args       = args
#         self.kwargs     = kwargs
#         self.is_running = False
#         self.start()

#     def _run(self):
#         self.is_running = False
#         self.start()
#         self.function(*self.args, **self.kwargs)

#     def start(self):
#         if not self.is_running:
#             self._timer = Timer(self.interval, self._run)
#             self._timer.start()
#             self.is_running = True

#     def stop(self):
#         self._timer.cancel()
#         self.is_running = False

import time
from threading import Event, Thread

class RepeatedTimer:

    """Repeat `function` every `interval` seconds."""

    def __init__(self, interval, function, *args, **kwargs):
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.start = time.time()
        self.event = Event()
        self.thread = Thread(target=self._target)
        self.thread.start()

    def _target(self):
        while not self.event.wait(self._time):
            self.function(*self.args, **self.kwargs)

    @property
    def _time(self):
        return self.interval - ((time.time() - self.start) % self.interval)

    def stop(self):
        self.event.set()
        self.thread.join()

