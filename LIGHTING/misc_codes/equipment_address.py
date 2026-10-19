
class EQUIPMENT_ADDRESS():
    SCOPE = "10.126.240.122"
    
    AC_SOURCE = 12
    DC_SOURCE = 10
    
    ELOAD = 8

    POWER_METER_SOURCE = 2
    POWER_METER_LOAD_1 = 16
    POWER_METER_LOAD_2 = 10
    POWER_METER_LOAD_3 = 25
    POWER_METER_LOAD_4 = 6

    ELOAD_CHANNEL_1 = 1
    ELOAD_CHANNEL_2 = 3
    ELOAD_CHANNEL_3 = 5
    ELOAD_CHANNEL_4 = 7


    SIG_GEN = 19
    DC_SOURCE_DIMMER = 30

    # Placeholders for fully enclosed equipment classes
    ARDUINO = "COM3" # Placeholder COM port
    LECROY_SCOPE = "169.254.1.1" # Placeholder IP
    EMI_TESTER = "GPIB0::X::INSTR" # Placeholder GPIB
    YOKOGAWA_SCOPE = "169.254.1.2" # Placeholder IP
    KEYSIGHT_33500B = "USB0::X::INSTR" # Placeholder USB
    KEITHLEY_2230G = "USB0::Y::INSTR" # Placeholder USB
    FLUKE_8808A = "COM4" # Placeholder COM port
    HV_DC_SOURCE = None # Magna-Power SL1000-1.5: GPIB number, VISA string, or None = auto-detect by *IDN?


    # LSCOPE = "169.254.94.235"
    # SCOPE = "10.126.111.35"
    
    # AC_SOURCE = 5
    
    # POWER_METER_SOURCE = 11
    # POWER_METER_LOAD_1 = 1
    # POWER_METER_LOAD_2 = 1
    # POWER_METER_DIM = 21
    
    # SIG_GEN = '11'
    
    # ELOAD = 8
    # ELOAD_CHANNEL = 7

    # ARDUINO_COMM_PORT = 5