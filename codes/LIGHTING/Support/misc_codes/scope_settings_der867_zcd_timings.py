class SCOPE_CONFIG():

    TRIGGER_CHANNEL = 2
    TRIGGER_LEVEL = 1
    TRIGGER_EDGE = 'POS'

    TIME_POSTIION = 10
    TIME_SCALE = 1

    ZOOM_ENABLE = False
    ZOOM_POS = 50
    ZOOM_REL_SCALE = 1

    global CH1_ENABLE, CH2_ENABLE, CH3_ENABLE, CH4_ENABLE
    CH1_ENABLE = 'ON'
    CH2_ENABLE = 'ON'
    CH3_ENABLE = 'ON'
    CH4_ENABLE = 'ON'

    class CH1():
        REL_X_POS = 20
        ENABLE = CH1_ENABLE

        SCALE = 100
        POSITION = -1
        BANDWIDTH = 20
        LABEL = "Input Voltage"
        MEASURE = "MAX,RMS,FREQ"
        COLOR = "YELLOW"
        COUPLING = "AC"
        OFFSET = 0

    class CH2():
        REL_X_POS = 40
        ENABLE = CH2_ENABLE

        SCALE = 2
        POSITION = 3
        BANDWIDTH = 20
        LABEL = "ZCD"
        MEASURE = "MAX,MIN"
        COLOR = "ORANGE"
        COUPLING = "DCLimit"
        OFFSET = 0

    class CH3():
        REL_X_POS = 60
        ENABLE = CH3_ENABLE

        SCALE = 1
        POSITION = -1
        BANDWIDTH = 20
        LABEL = "RelayON Pulse"
        MEASURE = "MAX,MIN"
        COLOR = "LIGHT_BLUE"
        COUPLING = "DCLimit"
        OFFSET = 0

    class CH4():
        REL_X_POS = 80
        ENABLE = CH4_ENABLE
        
        SCALE = 10
        POSITION = -1
        BANDWIDTH = 20
        LABEL = "Input Current"
        MEASURE = "MAX,MIN"
        COLOR = "PINK"
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


class SCOPE_CONFIG_LED():

    TRIGGER_CHANNEL = 2
    TRIGGER_LEVEL = 1
    TRIGGER_EDGE = 'POS'

    TIME_POSTIION = 10
    TIME_SCALE = 1

    ZOOM_ENABLE = False
    ZOOM_POS = 50
    ZOOM_REL_SCALE = 1

    global CH1_ENABLE, CH2_ENABLE, CH3_ENABLE, CH4_ENABLE
    CH1_ENABLE = 'ON'
    CH2_ENABLE = 'ON'
    CH3_ENABLE = 'ON'
    CH4_ENABLE = 'ON'

    class CH1():
        REL_X_POS = 20
        ENABLE = CH1_ENABLE

        SCALE = 100
        POSITION = -1
        BANDWIDTH = 20
        LABEL = "Input Voltage"
        MEASURE = "MAX,RMS,FREQ"
        COLOR = "YELLOW"
        COUPLING = "AC"
        OFFSET = 0

    class CH2():
        REL_X_POS = 40
        ENABLE = CH2_ENABLE

        SCALE = 2
        POSITION = 3
        BANDWIDTH = 20
        LABEL = "ZCD"
        MEASURE = "MAX,MIN"
        COLOR = "ORANGE"
        COUPLING = "DCLimit"
        OFFSET = 0

    class CH3():
        REL_X_POS = 60
        ENABLE = CH3_ENABLE

        SCALE = 1
        POSITION = -1
        BANDWIDTH = 20
        LABEL = "RelayON Pulse"
        MEASURE = "MAX,MIN"
        COLOR = "LIGHT_BLUE"
        COUPLING = "DCLimit"
        OFFSET = 0

    class CH4():
        REL_X_POS = 80
        ENABLE = CH4_ENABLE
        
        SCALE = 6
        POSITION = -1
        BANDWIDTH = 20
        LABEL = "Input Current"
        MEASURE = "MAX,MIN"
        COLOR = "PINK"
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

class SCOPE_CONFIG_FAN():

    TRIGGER_CHANNEL = 2
    TRIGGER_LEVEL = 1
    TRIGGER_EDGE = 'POS'

    TIME_POSTIION = 10
    TIME_SCALE = 1

    ZOOM_ENABLE = False
    ZOOM_POS = 50
    ZOOM_REL_SCALE = 1

    global CH1_ENABLE, CH2_ENABLE, CH3_ENABLE, CH4_ENABLE
    CH1_ENABLE = 'ON'
    CH2_ENABLE = 'ON'
    CH3_ENABLE = 'ON'
    CH4_ENABLE = 'ON'

    class CH1():
        REL_X_POS = 20
        ENABLE = CH1_ENABLE

        SCALE = 100
        POSITION = -1
        BANDWIDTH = 20
        LABEL = "Input Voltage"
        MEASURE = "MAX,RMS,FREQ"
        COLOR = "YELLOW"
        COUPLING = "AC"
        OFFSET = 0

    class CH2():
        REL_X_POS = 40
        ENABLE = CH2_ENABLE

        SCALE = 2
        POSITION = 3
        BANDWIDTH = 20
        LABEL = "ZCD"
        MEASURE = "MAX,MIN"
        COLOR = "ORANGE"
        COUPLING = "DCLimit"
        OFFSET = 0

    class CH3():
        REL_X_POS = 60
        ENABLE = CH3_ENABLE

        SCALE = 1
        POSITION = -1
        BANDWIDTH = 20
        LABEL = "RelayON Pulse"
        MEASURE = "MAX,MIN"
        COLOR = "LIGHT_BLUE"
        COUPLING = "DCLimit"
        OFFSET = 0

    class CH4():
        REL_X_POS = 80
        ENABLE = CH4_ENABLE
        
        SCALE = 0.2
        POSITION = -1
        BANDWIDTH = 20
        LABEL = "Input Current"
        MEASURE = "MAX,MIN"
        COLOR = "PINK"
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