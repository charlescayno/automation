class SCOPE_CONFIG():

    TRIGGER_CHANNEL = 4
    TRIGGER_LEVEL = 3.9
    TRIGGER_EDGE = 'POS'

    TIME_POSTIION = 50
    TIME_SCALE = 0.1

    ZOOM_ENABLE = False
    ZOOM_POS = 50
    ZOOM_REL_SCALE = 1

    global CH1_ENABLE, CH2_ENABLE, CH3_ENABLE, CH4_ENABLE
    CH1_ENABLE = 'ON'
    CH2_ENABLE = 'OFF'
    CH3_ENABLE = 'ON'
    CH4_ENABLE = 'ON'

    class CH1():
        REL_X_POS = 20
        ENABLE = CH1_ENABLE

        SCALE = 1
        POSITION = 0
        BANDWIDTH = 20
        LABEL = "Vcoil"
        MEASURE = "MAX,MEAN"
        COLOR = "LIGHT_BLUE"
        COUPLING = "DCLimit"
        OFFSET = 0

    class CH2():
        REL_X_POS = 40
        ENABLE = CH2_ENABLE

        SCALE = 1
        POSITION = 0
        BANDWIDTH = 20
        LABEL = "V_Balance_Coil"
        MEASURE = "RMS,PDELta"
        COLOR = "YELLOW"
        COUPLING = "DCLimit"
        OFFSET = 0

    class CH3():
        REL_X_POS = 60
        ENABLE = CH3_ENABLE

        SCALE = 1
        POSITION = 0
        BANDWIDTH = 500
        LABEL = "Icoil"
        MEASURE = "MAX,RMS,PDELta"
        COLOR = "PINK"
        COUPLING = "DCLimit"
        OFFSET = 0

    class CH4():
        REL_X_POS = 80
        ENABLE = CH4_ENABLE
        
        SCALE = 1
        POSITION = 0
        BANDWIDTH = 20
        LABEL = "Vgs"
        MEASURE = "MAX,PDELta,FREQ"
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