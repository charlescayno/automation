from enum import Enum
from msilib import PID_APPNAME

class HID_SMBUS_DEFINITIONS(Enum):
    """ Includes the definitions needed for using the SLABHIDtoSMBus dll
    """
    
    # CP2112 Vendor ID
    VID = 0x10C4
    PID = 0xEA90

    #################################################################### 
    # RETURN CODE DEFINITIONS                                          #
    #################################################################### 
    # HID_SMBUS_STATUS return codes
    SUCCESS							=       0x00
    DEVICE_NOT_FOUND				=       0x01
    INVALID_HANDLE					=       0x02
    INVALID_DEVICE_OBJECT			=       0x03
    INVALID_PARAMETER				=       0x04
    INVALID_REQUEST_LENGTH			=       0x05

    READ_ERROR						=       0x10
    WRITE_ERROR						=       0x11
    READ_TIMED_OUT					=       0x12
    WRITE_TIMED_OUT					=       0x13
    DEVICE_IO_FAILED				=       0x14
    DEVICE_ACCESS_ERROR				=       0x15
    DEVICE_NOT_SUPPORTED			=       0x16

    UNKNOWN_ERROR					=       0xFF


    # HID_SMBUS_TRANSFER_S0
    S0_IDLE							=       0x00
    S0_BUSY							=       0x01
    S0_COMPLETE						=       0x02
    S0_ERROR						=       0x03


    # HID_SMBUS_TRANSFER_S1

    # HID_SMBUS_TRANSFER_S0 = HID_SMBUS_S0_BUSY
    S1_BUSY_ADDRESS_ACKED			=       0x00
    S1_BUSY_ADDRESS_NACKED			=       0x01
    S1_BUSY_READING					=       0x02
    S1_BUSY_WRITING					=       0x03

    # HID_SMBUS_TRANSFER_S0 = HID_SMBUS_S0_ERROR
    S1_ERROR_TIMEOUT_NACK			=       0x00
    S1_ERROR_TIMEOUT_BUS_NOT_FREE	=       0x01
    S1_ERROR_ARB_LOST				=       0x02
    S1_ERROR_READ_INCOMPLETE		=       0x03
    S1_ERROR_WRITE_INCOMPLETE		=       0x04
    S1_ERROR_SUCCESS_AFTER_RETRY	=       0x05

    #################################################################### 
    # STRING DEFINITIONS                                               #
    #################################################################### 
    # SMbus Configuration Limits
    MIN_BIT_RATE					=       1
    MIN_TIMEOUT						=       0
    MAX_TIMEOUT						=       1000
    MAX_RETRIES						=       1000
    MIN_ADDRESS						=       0x02
    MAX_ADDRESS						=       0xFE

    # Read/Write Limits
    MIN_READ_REQUEST_SIZE			=       1
    MAX_READ_REQUEST_SIZE			=       512
    MIN_TARGET_ADDRESS_SIZE			=       1
    MAX_TARGET_ADDRESS_SIZE			=       16
    MAX_READ_RESPONSE_SIZE			=       61
    MIN_WRITE_REQUEST_SIZE			=       1
    MAX_WRITE_REQUEST_SIZE			=       13

    #################################################################### 
    # GPIO DEFINITIONS                                          #
    ####################################################################

    # GPIO Pin Direction Bit Value
    DIRECTION_INPUT					=       0
    DIRECTION_OUTPUT				=       1

    # GPIO Pin Mode Bit Value
    MODE_OPEN_DRAIN					=       0
    MODE_PUSH_PULL					=       1

    # GPIO Function Bitmask
    MASK_FUNCTION_GPIO_7_CLK		=       0x01
    MASK_FUNCTION_GPIO_0_TXT		=       0x02
    MASK_FUNCTION_GPIO_1_RXT		=       0x04

    # GPIO Function Bit Value
    GPIO_FUNCTION					=       0
    SPECIAL_FUNCTION				=       1

    # GPIO Pin Bitmask
    MASK_GPIO_0						=       0x01
    MASK_GPIO_1						=       0x02
    MASK_GPIO_2						=       0x04
    MASK_GPIO_3						=       0x08
    MASK_GPIO_4						=       0x10
    MASK_GPIO_5						=       0x20
    MASK_GPIO_6						=       0x40
    MASK_GPIO_7						=       0x80

    #################################################################### 
    # PART NUMBER DEFINITIONS                                          #
    ####################################################################
    # Part Numbers
    PART_CP2112						=       0x0C

    #################################################################### 
    # USER CUSTOMIZATION DEFINITIONS                                          #
    ####################################################################
    # User-Customizable Field Lock Bitmasks
    LOCK_VID						=       0x01
    LOCK_PID						=       0x02
    LOCK_POWER						=       0x04
    LOCK_POWER_MODE					=       0x08
    LOCK_RELEASE_VERSION			=       0x10
    LOCK_MFG_STR					=       0x20
    LOCK_PRODUCT_STR				=       0x40
    LOCK_SERIAL_STR					=       0x80

    # Field Lock Bit Values
    LOCK_UNLOCKED					=       1
    LOCK_LOCKED						=       0

    # Power Max Value (500 mA)
    BUS_POWER_MAX					=       0xFA

    # Power Modes
    BUS_POWER						=       0x00
    SELF_POWER_VREG_DIS				=       0x01
    SELF_POWER_VREG_EN				=       0x02

    # USB Config Bitmasks
    SET_VID							=       0x01
    SET_PID							=       0x02
    SET_POWER						=       0x04
    SET_POWER_MODE					=       0x08
    SET_RELEASE_VERSION				=       0x10

    # USB Config Bit Values
    SET_IGNORE						=       0
    SET_PROGRAM						=       1

    # String Lengths
    CP2112_MFG_STRLEN				=       30
    CP2112_PRODUCT_STRLEN			=       30
    CP2112_SERIAL_STRLEN			=       30 