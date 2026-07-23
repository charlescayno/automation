
from powi.equipment import Oscilloscope
from misc_codes.equipment_address import *
from misc_codes.scope_settings_fod import *

scope = Oscilloscope(EQUIPMENT_ADDRESS.SCOPE)

def scope_settings(SCOPE_CONFIG):

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
    scope_settings(SCOPE_CONFIG_PIHI_ATE)

if __name__ == "__main__":
    main()