from misc_codes.equipment_settings import *
from misc_codes.general_settings import *

def scope_settings():
    
    scope.channel_settings(state='ON', channel=1, scale=0.4, position=-4, label="Vfb",
                            color='YELLOW', rel_x_position=20, bandwidth=20, coupling='DCLimit', offset=0)
    
    
    scope.channel_settings(state='OFF', channel=2, scale=2, position=-4, label="VDS",
                            color='PINK', rel_x_position=40, bandwidth=20, coupling='DCLimit', offset=0)
    
    
    scope.channel_settings(state='ON', channel=3, scale=2, position=-4, label="Vaux",
                            color='ORANGE', rel_x_position=60, bandwidth=20, coupling='DCLimit', offset=0)
    
    
    scope.channel_settings(state='ON', channel=4, scale=10, position=-4, label="Vout",
                            color='LIGHT_BLUE', rel_x_position=80, bandwidth=20, coupling='DCLimit', offset=0)
    
    
    scope.measure(1, "MAX,RMS")
    # scope.measure(2, "MAX,RMS")
    scope.measure(3, "MAX,RMS")
    scope.measure(4, "MAX,RMS")

    scope.time_position(10)
    
    scope.record_length(50E6)
    
    scope.time_scale(1)

    # scope.remove_zoom()
    # scope.add_zoom(rel_pos=21.727, rel_scale=1)
    
    trigger_channel = 1
    trigger_level = 1
    trigger_edge = 'POS'
    scope.edge_trigger(trigger_channel, trigger_level, trigger_edge)

    scope.stop()



def main():

    scope_settings()
        
if __name__ == "__main__":

    main()
