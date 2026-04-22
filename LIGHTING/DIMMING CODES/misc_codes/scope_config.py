class SCOPE_CONFIG():

    TRIGGER_CHANNEL = 1
    TRIGGER_LEVEL = 3.2
    TRIGGER_EDGE = 'POS'

    TIME_POSTIION = 50
    TIME_SCALE = 1e-03

    ZOOM_ENABLE = False
    ZOOM_POS = 50
    ZOOM_REL_SCALE = 1

    global CH1_ENABLE, CH2_ENABLE, CH3_ENABLE, CH4_ENABLE
    CH1_ENABLE = 'ON'
    CH2_ENABLE = 'ON'
    CH3_ENABLE = 'OFF'
    CH4_ENABLE = 'ON'


    class CH1():
        REL_X_POS = 20
        ENABLE = CH1_ENABLE

        SCALE = 1
        POSITION = 0
        BANDWIDTH = 20
        LABEL = "Va"
        MEASURE = "MAX,MIN,RMS,MEAN"
        COLOR = "PINK"
        COUPLING = "DCLimit"
        OFFSET = 0

    class CH2():
        REL_X_POS = 40
        ENABLE = CH2_ENABLE

        SCALE = 1
        POSITION = 0
        BANDWIDTH = 20
        LABEL = "Vfod"
        MEASURE = "MAX,MIN,RMS,MEAN"
        COLOR = "YELLOW"
        COUPLING = "DCLimit"
        OFFSET = 0

    class CH3():
        REL_X_POS = 60
        ENABLE = CH3_ENABLE

        SCALE = 1
        POSITION = 0
        BANDWIDTH = 20
        LABEL = "Vb"
        MEASURE = "MAX,MIN,RMS,MEAN"
        COLOR = "PINK"
        COUPLING = "DCLimit"
        OFFSET = 0

    class CH4():
        REL_X_POS = 80
        ENABLE = CH4_ENABLE
        
        SCALE = 1
        POSITION = 0
        BANDWIDTH = 20
        LABEL = "Vb"
        MEASURE = "MAX,MIN,RMS,MEAN"
        COLOR = "LIGHT_BLUE"
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

class SCOPE_CONFIG_SRFET_VDS():

    TRIGGER_CHANNEL = 1
    TRIGGER_LEVEL = 20
    TRIGGER_EDGE = 'POS'

    TIME_POSTIION = 50
    TIME_SCALE = 20e-06

    ZOOM_ENABLE = False
    ZOOM_POS = 50
    ZOOM_REL_SCALE = 1

    global CH1_ENABLE, CH2_ENABLE, CH3_ENABLE, CH4_ENABLE
    CH1_ENABLE = 'ON'
    CH2_ENABLE = 'OFF'
    CH3_ENABLE = 'OFF'
    CH4_ENABLE = 'OFF'


    class CH1():
        REL_X_POS = 20
        ENABLE = CH1_ENABLE

        SCALE = 20
        POSITION = -4
        BANDWIDTH = 500
        LABEL = "SRFET VDS"
        MEASURE = "MAX,MIN"
        COLOR = "YELLOW"
        COUPLING = "DCLimit"
        OFFSET = 0

    class CH2():
        REL_X_POS = 40
        ENABLE = CH2_ENABLE

        SCALE = 100
        POSITION = -4
        BANDWIDTH = 500
        LABEL = "VDS"
        MEASURE = "MAX,MIN,RMS"
        COLOR = "YELLOW"
        COUPLING = "DC"
        OFFSET = 0

    class CH3():
        REL_X_POS = 60
        ENABLE = CH3_ENABLE

        SCALE = 0.5
        POSITION = -4
        BANDWIDTH = 20
        LABEL = "IOUT"
        MEASURE = "MAX,PDELTA,RMS"
        COLOR = "PINK"
        COUPLING = "DCLimit"
        OFFSET = 0

    class CH4():
        REL_X_POS = 80
        ENABLE = CH4_ENABLE
        
        SCALE = 4
        POSITION = -4
        BANDWIDTH = 20
        LABEL = "VOUT"
        MEASURE = "MAX,MIN,RMS"
        COLOR = "GREEN"
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

class SCOPE_CONFIG_PRIMARY_VDS():

    TRIGGER_CHANNEL = 1
    TRIGGER_LEVEL = 20
    TRIGGER_EDGE = 'POS'

    TIME_POSTIION = 50
    TIME_SCALE = 20e-06

    ZOOM_ENABLE = False
    ZOOM_POS = 50
    ZOOM_REL_SCALE = 1

    global CH1_ENABLE, CH2_ENABLE, CH3_ENABLE, CH4_ENABLE
    CH1_ENABLE = 'ON'
    CH2_ENABLE = 'OFF'
    CH3_ENABLE = 'OFF'
    CH4_ENABLE = 'OFF'


    class CH1():
        REL_X_POS = 20
        ENABLE = CH1_ENABLE

        SCALE = 100
        POSITION = -4
        BANDWIDTH = 500
        LABEL = "PRIMARY VDS"
        MEASURE = "MAX,MIN"
        COLOR = "LIGHT_BLUE"
        COUPLING = "DCLimit"
        OFFSET = 0

    class CH2():
        REL_X_POS = 40
        ENABLE = CH2_ENABLE

        SCALE = 100
        POSITION = -4
        BANDWIDTH = 500
        LABEL = "VDS"
        MEASURE = "MAX,MIN,RMS"
        COLOR = "YELLOW"
        COUPLING = "DC"
        OFFSET = 0

    class CH3():
        REL_X_POS = 60
        ENABLE = CH3_ENABLE

        SCALE = 0.5
        POSITION = -4
        BANDWIDTH = 20
        LABEL = "IOUT"
        MEASURE = "MAX,PDELTA,RMS"
        COLOR = "PINK"
        COUPLING = "DCLimit"
        OFFSET = 0

    class CH4():
        REL_X_POS = 80
        ENABLE = CH4_ENABLE
        
        SCALE = 4
        POSITION = -4
        BANDWIDTH = 20
        LABEL = "VOUT"
        MEASURE = "MAX,MIN,RMS"
        COLOR = "GREEN"
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
