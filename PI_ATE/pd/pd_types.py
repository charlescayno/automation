import ctypes as ct
from ctypes import c_uint32

from enum import Enum


# Enumeration of the commands supported in PD_CTRL register
###############################################################################################
#  PD Commands                                                                                #
###############################################################################################

class PD_COMMAND(Enum):
    SET_TYPE_C_DEFAULT_RP           = 0
    SET_TYPE_C_1_5A_RP              = 1
    SET_TYPE_C_3A_RP                = 2
    SEND_DR_SWAP                    = 5
    SEND_PR_SWAP                    = 6
    TURN_ON_VCONN                   = 7
    TURN_OFF_VCONN                  = 8
    SEND_VCONN_SWAP                 = 9
    GET_SRC_CAP                     = 10
    GET_SNK_CAP                     = 11
    SEND_GOTOMIN                    = 12
    SEND_HARD_RESET                 = 13
    SEND_SOFT_RESET_SOP             = 14
    SEND_CABLE_RESET                = 0xF
    SEND_EC_INIT_COMPLETE           = 0x10
    DISABLE_PORT                    = 17
    SEND_SOFT_RESET_SOP_PRIME       = 18
    SEND_SOFT_RESET_SOP_D_PRIME     = 19
    CHANGE_PORT_PARAMS              = 20
    ABORT_PD_CMD                    = 21
    GET_EXTD_SRC_CAP                = 22
    GET_STATUS                      = 23
    SEND_NOT_SUPPORTED              = 24
    GET_PPS_STATUS                  = 25
    RSVD1                           = 26
    RSVD2                           = 27
    SEND_OV_NOTIFICATION            = 28
    SEND_OC_NOTIFICATION            = 29
    SEND_OT_NOTIFICATION            = 30
    SEND_CCG_ALIVE                  = 0x1F
    READ_SRC_PDO                    = 0x20
    READ_SNK_PDO                    = 33
    READ_EXTD_SRC_CAP               = 36
    WR_EXTD_SRC_CAP                 = 37


###############################################################################################
#  PDO definitions                                                           #
###############################################################################################

class PDO_SUPPLY_TYPE(Enum):
    FIXED = 0
    BATTERY = 1
    VARIABLE = 2
    AUGMENTED = 3


###############################################################################################
#  PD Multipliers                                                              #
###############################################################################################

class PD_MULTIPLIER(Enum):
    PPS_MAX_VOLT_MULTIPLIER = 100
    PPS_MIN_VOLT_MULTIPLIER = 100
    PPS_MAX_CURRENT_MULTIPLIER = 50
    FPDO_SUPPLY_VOLT_MULTIPLIER = 50
    FPDO_SUPPLY_MAX_CURRENT_MULTIPLIER = 10
    POWER_DIVIDER = 100
    VBUS_ = 1000
    TIME_MS_TO_S = 1000

###############################################################################################
#  CYPD2122 - CCG2 HPI v1 Register                                                            #
###############################################################################################
# Import as CY_PD_REG
class HPI_V1_REG(Enum):
    DEVICE_MODE_ADDR                = 0
    BOOT_MODE_REASON                = 1
    SILICON_ID                      = 2
    INTR_REG_ADDR                   = 6
    JUMP_TO_BOOT_REG_ADDR           = 7
    RESET_ADDR                      = 8
    ENTER_FLASH_MODE_ADDR           = 10
    VALIDATE_FW_ADDR                = 11
    FLASH_READ_WRITE_ADDR           = 12
    GET_VERSION                     = 0x10
    U_VDM_CTRL_ADDR                 = 0x20
    READ_PD_PROFILE                 = 34
    EFFECTIVE_SOURCE_PDO_MASK       = 36
    EFFECTIVE_SINK_PDO_MASK         = 37
    SELECT_SOURCE_PDO               = 38
    SELECT_SINK_PDO                 = 39
    PD_CONTROL                      = 40
    PD_STATUS                       = 44
    TYPE_C_STATUS                   = 48
    CURRENT_PDO                     = 52
    CURRENT_RDO                     = 56
    CURRENT_CABLE_VDO               = 60
    HPD_MODE                        = 68
    DP_MUX_SELECT                   = 69
    EVENT_MASK                      = 72
    SRC_PDO                         = 84
    SRC_PDO_CNT                     = 112
    MEASURE_VBUS                    = 113
    RESPONSE_ADDR                   = 126
    BOOTDATA_MEMORY_ADDR            = 0x80
    FWDATA_MEMORY_ADDR              = 192

###############################################################################################
#  CYPD2122 - CCG2 HPI Response                                                               #
###############################################################################################
# Import as CY_PD_RESP

class HPI_RESPONSE(Enum):
    NO_RESPONSE                     = 0
    SUCCESS                         = 2
    FLASH_DATA_AVAILABLE            = 3
    INVALID_COMMAND                 = 5
    COLLISION_DETECTED              = 6
    FLASH_UPDATE_FAILED             = 7
    INVALID_FW                      = 8
    INVALID_ARGUMENTS               = 9
    NOT_SUPPORTED                   = 10
    TRANSACTION_FAILED              = 12
    PD_COMMAND_FAILED               = 13
    UNDEFINED                       = 14
    RESET_COMPLETE                  = 0x80
    MESSAGE_QUEUE_OVERFLOW          = 129
    OVER_CURRENT_DETECTED           = 130
    OVER_VOLTAGE_DETECTED           = 131
    TYPC_C_CONNECTED                = 132
    TYPE_C_DISCONNECTED             = 133
    PD_CONTRACT_ESTABLISHED         = 134
    DR_SWAP                         = 135
    PR_SWAP                         = 136
    VCON_SWAP                       = 137
    PS_RDY                          = 138
    GOTOMIN                         = 139
    ACCEPT_MESSAGE                  = 140
    REJECT_MESSAGE                  = 141
    WAIT_MESSAGE                    = 142
    HARD_RESET                      = 143
    VDM_RECEIVED                    = 144
    SRC_CAP_RCVD                    = 145
    SINK_CAP_RCVD                   = 146
    DP_ALTERNATE_MODE               = 147
    DP_DEVICE_CONNECTED             = 148
    DP_DEVICE_NOT_CONNECTED         = 149
    DP_SID_NOT_FOUND                = 150
    MULTIPLE_SVID_DISCOVERED        = 151
    DP_FUNCTION_NOT_SUPPORTED       = 152
    DP_PORT_CONFIG_NOT_SUPPORTED    = 153
    HARD_RESET_SENT                 = 154
    SOFT_RESET_SENT                 = 155
    CABLE_RESET_SENT                = 156
    SOURCE_DISABLED_STATE_ENTERED   = 157
    SENDER_RESPONSE_TIMER_TIMEOUT   = 158
    NO_VDM_RESPONSE_RECEIVED        = 159
    UNEXPECTED_VOLTAGE_ON_VBUS      = 160
    TYPE_C_ERROR_RECOVERY           = 161
    EMCA_DETECTED                   = 166
    CABLE_DISC_FAILED               = 167
    RP_CHANGE_DETECTED              = 170
    SYS_EVT_VSEL                    = 178


###############################################################################################
#  CYPD2122 - CCG2 Object definitions                                                           #
###############################################################################################

# Template
# # REG description
# class REG_bits(ct.LittleEndianStructure):
#     _fields_ = [("",        c_uint32,    30),
#                 ("",     c_uint32,    2)]
# class REG(ct.Union):
#     _fields_ = [("bits", REG_bits),
#                 ("asbyte", c_uint32)]

# Structures taken from 
# https://stackoverflow.com/questions/142812/does-python-have-a-bitfield-type

# General purpose Power Data Object
class PDO_bits(ct.LittleEndianStructure):
    _fields_ = [("reserved",    c_uint32,    30),
                ("supply_type", c_uint32,    2)
    ]
class PDO(ct.Union):
    _fields_ = [("bits", PDO_bits),
                ("asbyte", c_uint32)]


# Fixed Power Data Object for Supplies
class FPDOSupply_bits(ct.LittleEndianStructure):
    _fields_ = [
        ("max_current",         c_uint32, 10),  # Max current in 10mA units
        ("voltage",             c_uint32, 10),  # Voltage in 50mV units
        ("peak_current",        c_uint32, 2),   # Peak I (divergent from Ioc ratings)
        ("reserved",            c_uint32, 3),   # Reserved
        ("data_role_swap",      c_uint32, 1),   # Data role swap supported
        ("usb_comm_capable",    c_uint32, 1),   # USB communications capable
        ("externally_powered",  c_uint32, 1),   # Externally powered
        ("usb_suspend_support", c_uint32, 1),   # USB Suspend Supported
        ("dual_role_power",     c_uint32, 1),   # Dual-Role power  - supports PR swap
        ("supply_type",         c_uint32, 2)]   # (Fixed Supply)
class FPDOSupply(ct.Union):
    _fields_ = [("bits", FPDOSupply_bits),
                ("asbyte", c_uint32)]


# Fixed Power Data Object for Sinks
class FPDOSink_bits(ct.LittleEndianStructure):
    _fields_ = [
        ("operational_current", c_uint32, 10),  # Operational current in 10mA units
        ("voltage",             c_uint32, 10),  # Voltage in 50mV units
        ("reserved",            c_uint32, 5),   # Reserved
        ("data_role_swap",      c_uint32, 1),   # Data role swap supported
        ("usb_comm_capable",    c_uint32, 1),   # USB communications capable
        ("externally_powered",  c_uint32, 1),   # Externally powered
        ("higher_capability",   c_uint32, 1),   # Needs more than vSafe5V
        ("dual_role_power",     c_uint32, 1),   # Dual-Role power - supports PR swap
        ("supply_type",         c_uint32, 2)]   # (Fixed Supply)
class FPDOSink(ct.Union):
    _fields_ = [("bits", FPDOSink_bits),
                ("asbyte", c_uint32)]


# Augmented Power Data Object
class APDO_bits(ct.LittleEndianStructure):
    _fields_ = [
        ("reserved",            c_uint32, 28),  # APDO-Defined Bits 
        ("apdo_type",           c_uint32, 2),   # Augmented Type
        ("supply_type",         c_uint32, 2)]   # (Augmented PDO)
class APDO(ct.Union):
    _fields_ = [("bits", APDO_bits),
                ("asbyte", c_uint32)]


# Programmable Power Supply Data Object
class PPSAPDO_bits(ct.LittleEndianStructure):
    _fields_ = [
        ("max_current",         c_uint32, 7),   # Max current in 50mA units
        ("reserved0",           c_uint32, 1),   # Reserved
        ("min_voltage",         c_uint32, 8),   # Min voltage in 100mV unit
        ("reserved1",           c_uint32, 1),   # Reserved
        ("max_voltage",         c_uint32, 8),   # Max voltage in 100mV units
        ("reserved2",           c_uint32, 3),   # Reserved
        ("apdo_type",           c_uint32, 2),   # (PPS: 0)
        ("supply_type",         c_uint32, 2)]   # (Augmented PDO)
class PPSAPDO(ct.Union):
    _fields_ = [("bits", PPSAPDO_bits),
                ("asbyte", c_uint32)]


# Fixed Voltage Request Data Object
class FVRDO_bits(ct.LittleEndianStructure):
    _fields_ = [
        ("iout_max",            c_uint32, 10),  # Min/Max current in 10mA units
        ("iout_operating",      c_uint32, 10),  # Operating current in 10mA units
        ("reserved0",           c_uint32, 4),   # Reserved - set to zero
        ("usb_suspend",         c_uint32, 1),   # Set when the sink wants to continue
        #                                         the contract during USB suspend
        #                                         (i.e. charging battery)
        ("usb_comm_cap",        c_uint32, 1),   # USB communications capable
        ("cap_mismatch",        c_uint32, 1),   # Set if the sink cannot satisfy its
        #                                         power requirements from caps offered
        ("give_back",           c_uint32, 1),   # Whether the sink will respond to
        #                                         the GotoMin message
        ("object_position",     c_uint32, 3),   # Index of source cap being requested
        ("reserved1",           c_uint32, 1)]   # Reserved
class FVRDO(ct.Union):
    _fields_ = [
        ("bits", FVRDO_bits),
        ("asbyte", c_uint32)]


# PPSRDO description
class PPSRDO_bits(ct.LittleEndianStructure):
    _fields_ = [
        ("operating_current",   c_uint32, 7),   # Operating current in 50mA units
        ("reserved0",           c_uint32, 2),   # Reserved
        ("operating_voltage",   c_uint32, 11),  # Requested voltage in 20mV units
        ("reserved1",           c_uint32, 4),   # Reserved
        ("no_usb_suspend",      c_uint32, 1),   # Set when the sink wants to continue
        #                                         the contract during USB suspend
        #                                         (i.e. charging battery)
        ("usb_comm_capable",    c_uint32, 1),   # USB communications capable
        ("capability_mismatch", c_uint32, 1),   # Set if the sink cannot satisfy its
        #                                         power requirements from caps offered
        ("reserved2",           c_uint32, 1),   # Reserved
        ("object_position",     c_uint32, 3),   # Index of source cap being requested
        ("reserved3",           c_uint32, 1)]   # Reserved
class PPSRDO(ct.Union):
    _fields_ = [("bits", PPSRDO_bits),
        ("asbyte", c_uint32)]


# UVDM object
class UVDM_bits(ct.LittleEndianStructure):
    _fields_ = [
        ("vendor_defined",      c_uint32, 15),  # Defined by the vendor
        ("vdm_type",            c_uint32, 1),   # Unstructured or structured msg header
        ("vendor_id",           c_uint32, 16)]  # Unique 16-bit unsigned integer
        #                                         assigned by the USB-IF
class UVDM(ct.Union):
    _fields_ = [
        ("bits", UVDM_bits),
        ("asbyte", c_uint32)]