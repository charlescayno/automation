
from misc_codes.equipment_settings import *

scope = Oscilloscope(EQUIPMENT_ADDRESS.SCOPE)

class SCOPE_CONFIG():

    """
        MEASUREMENT SETTINGS OPTIONS: "MAX,MIN,RMS,MEAN,PDELta"
        HIGH | LOW | AMPLitude | MAXimum | MINimum | PDELta |
                MEAN | RMS | STDDev | POVershoot | NOVershoot | AREA |
                RTIMe | FTIMe | PPULse | NPULse | PERiod | FREQuency |
                PDCYcle | NDCYcle | CYCarea | CYCMean | CYCRms |
                CYCStddev | PULCnt | DELay | PHASe | BWIDth | PSWitching |
                NSWitching | PULSetrain | EDGecount | SHT | SHR | DTOTrigger |
                PROBemeter | SLERising | SLEFalling
    """
    """
        COLOR OPTIONS:

        - LIGHT_BLUE
        - YELLOW
        - PINK
        - GREEN
        - BLUE
        - ORANGE

        returns : state of the channel ('ON' or 'OFF')
    """

    TRIGGER_CHANNEL = 2
    TRIGGER_LEVEL = 0.1
    TRIGGER_EDGE = 'POS'

    TIME_POSTIION = 50
    TIME_SCALE = 0.2

    ZOOM_ENABLE = False
    ZOOM_POS = 50
    ZOOM_REL_SCALE = 1

    class CH1():
        REL_X_POS = 20
        ENABLE = 'ON'
        COLOR = "PINK"

        ### PWM ####
        SCALE = 5
        POSITION = -4
        BANDWIDTH = 500
        LABEL = "PWM"
        MEASURE = "FREQ"
        COUPLING = "DCLimit"
        OFFSET = 0

        ### Vsense ####
        SCALE = 1
        POSITION = -3
        BANDWIDTH = 500
        LABEL = "Vsense"
        MEASURE = "MAX"
        COUPLING = "DCLimit"
        OFFSET = 0

        ### Isense ####
        SCALE = 1
        POSITION = -4
        BANDWIDTH = 20
        LABEL = "Isense"
        MEASURE = "MAX,MEAN,RMS,FREQ"
        COUPLING = "DCLimit"
        OFFSET = 0


    class CH2():
        REL_X_POS = 40
        ENABLE = 'ON'
        COLOR = "YELLOW"

        ### IOUT ####
        SCALE = 1
        POSITION = -4
        BANDWIDTH = 20
        LABEL = "IOUT"
        MEASURE = "MAX,MEAN,RMS"
        COUPLING = "DC"
        OFFSET = 0

        ### INPUT CURRENT ####
        SCALE = 1
        POSITION = -4
        BANDWIDTH = 20
        LABEL = "I_input"
        MEASURE = "MAX,MIN,MEAN,RMS"
        COUPLING = "DC"
        OFFSET = 0

    class CH3():
        REL_X_POS = 60
        ENABLE = 'ON'
        COLOR = "LIGHT_BLUE"

        ### VBusSen ####
        SCALE = 1
        POSITION = -4
        BANDWIDTH = 20
        LABEL = "VBusSen"
        MEASURE = "MAX,MEAN,RMS"
        COUPLING = "DCLimit"
        OFFSET = 0

        ### I_Tx_Coil ####
        SCALE = 1
        POSITION = 0
        BANDWIDTH = 500
        LABEL = "I_Tx_Coil"
        MEASURE = "MAX,PDEL,RMS"
        COUPLING = "DC"
        OFFSET = 0

    class CH4():
        REL_X_POS = 80
        ENABLE = 'ON'
        COLOR = "GREEN"
        
        ### Vin ####
        SCALE = 50
        POSITION = 0
        BANDWIDTH = 20
        LABEL = "VIN"
        MEASURE = "MAX,PDEL,RMS"
        COUPLING = "AC"
        OFFSET = 0

        ### Trig ####
        SCALE = 1
        POSITION = -4
        BANDWIDTH = 20
        LABEL = "Trig"
        MEASURE = "MAX"
        COUPLING = "DCLimit"
        OFFSET = 0

        ### PWM ####
        SCALE = 5
        POSITION = -4
        BANDWIDTH = 500
        LABEL = "PWM"
        MEASURE = "FREQ"
        COUPLING = "DCLimit"
        OFFSET = 0

    class CURSOR():

        class CURSOR_1():
            CHANNEL = 1
            ENABLE = False
            X1 = 0
            X2 = 0
            Y1 = 0
            Y2 = 0
            TYPE = 'HOR'
        
        class CURSOR_2():
            CHANNEL = 2
            ENABLE = False
            X1 = 0
            X2 = 0
            Y1 = 0
            Y2 = 0
            TYPE = 'HOR'
        
        class CURSOR_3():
            CHANNEL = 3
            ENABLE = False
            X1 = 0
            X2 = 0
            Y1 = 0
            Y2 = 0
            TYPE = 'HOR'
        
        class CURSOR_4():
            CHANNEL = 4
            ENABLE = False
            X1 = 0
            X2 = 0
            Y1 = 0
            Y2 = 0
            TYPE = 'HOR'

def scope_settings():

    CH1 = SCOPE_CONFIG.CH1
    CH2 = SCOPE_CONFIG.CH2
    CH3 = SCOPE_CONFIG.CH3
    CH4 = SCOPE_CONFIG.CH4
    CURSOR_1 = SCOPE_CONFIG.CURSOR.CURSOR_1
    CURSOR_2 = SCOPE_CONFIG.CURSOR.CURSOR_2
    CURSOR_3 = SCOPE_CONFIG.CURSOR.CURSOR_3
    CURSOR_4 = SCOPE_CONFIG.CURSOR.CURSOR_4
        
    scope.channel_settings(state=CH1.ENABLE, channel=1, scale=CH1.SCALE, position=CH1.POSITION, label=CH1.LABEL,
                            color=CH1.COLOR, rel_x_position=CH1.REL_X_POS, bandwidth=CH1.BANDWIDTH, coupling=CH1.COUPLING, offset=CH1.OFFSET)
    
    scope.channel_settings(state=CH2.ENABLE, channel=2, scale=CH2.SCALE, position=CH2.POSITION, label=CH2.LABEL,
                            color=CH2.COLOR, rel_x_position=CH2.REL_X_POS, bandwidth=CH2.BANDWIDTH, coupling=CH2.COUPLING, offset=CH2.OFFSET)
    
    scope.channel_settings(state=CH3.ENABLE, channel=3, scale=CH3.SCALE, position=CH3.POSITION, label=CH3.LABEL,
                            color=CH3.COLOR, rel_x_position=CH3.REL_X_POS, bandwidth=CH3.BANDWIDTH, coupling=CH3.COUPLING, offset=CH3.OFFSET)
    
    scope.channel_settings(state=CH4.ENABLE, channel=4, scale=CH4.SCALE, position=CH4.POSITION, label=CH4.LABEL,
                            color=CH4.COLOR, rel_x_position=CH4.REL_X_POS, bandwidth=CH4.BANDWIDTH, coupling=CH4.COUPLING, offset=CH4.OFFSET)
    
    if CH1.ENABLE != 'OFF': scope.measure(1, CH1.MEASURE)
    if CH2.ENABLE != 'OFF': scope.measure(2, CH2.MEASURE)
    if CH3.ENABLE != 'OFF': scope.measure(3, CH3.MEASURE)
    if CH4.ENABLE != 'OFF': scope.measure(4, CH4.MEASURE)

    scope.record_length(50E6)
    scope.time_position(SCOPE_CONFIG.TIME_POSTIION)
    scope.time_scale(SCOPE_CONFIG.TIME_SCALE)

    scope.remove_zoom()
    if SCOPE_CONFIG.ZOOM_ENABLE == True:
        scope.add_zoom(rel_pos=SCOPE_CONFIG.ZOOM_POS, rel_scale=SCOPE_CONFIG.ZOOM_REL_SCALE)
    
    trigger_channel = SCOPE_CONFIG.TRIGGER_CHANNEL
    trigger_level = SCOPE_CONFIG.TRIGGER_LEVEL
    trigger_edge = SCOPE_CONFIG.TRIGGER_EDGE
    scope.edge_trigger(trigger_channel, trigger_level, trigger_edge)

    scope.stop()

    if CURSOR_1.ENABLE: scope.cursor(channel=CURSOR_1.CHANNEL, cursor_set=1, X1=CURSOR_1.X1, X2=CURSOR_1.X2, Y1=CURSOR_1.Y1, Y2=CURSOR_1.Y2, type=CURSOR_1.TYPE)
    if CURSOR_2.ENABLE: scope.cursor(channel=CURSOR_2.CHANNEL, cursor_set=2, X1=CURSOR_2.X1, X2=CURSOR_2.X2, Y1=CURSOR_2.Y1, Y2=CURSOR_2.Y2, type=CURSOR_2.TYPE)
    if CURSOR_3.ENABLE: scope.cursor(channel=CURSOR_3.CHANNEL, cursor_set=3, X1=CURSOR_3.X1, X2=CURSOR_3.X2, Y1=CURSOR_3.Y1, Y2=CURSOR_3.Y2, type=CURSOR_3.TYPE)
    if CURSOR_4.ENABLE: scope.cursor(channel=CURSOR_4.CHANNEL, cursor_set=4, X1=CURSOR_4.X1, X2=CURSOR_4.X2, Y1=CURSOR_4.Y1, Y2=CURSOR_4.Y2, type=CURSOR_4.TYPE)

def main():
    scope_settings()


if __name__ == "__main__":
    main()