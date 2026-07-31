
from powi.equipment import PowerMeter
####################################################################################################################################################################

"""COMMS"""
source_power_meter_address = 30 
load_power_meter_address_1 = 20 
load_power_meter_address = 2
############################################################

"""EQUIPMENT INITIALIZE"""
pms = PowerMeter(source_power_meter_address)
pml = PowerMeter(load_power_meter_address)
# pml1 = PowerMeter(load_power_meter_address_1)

def main():
    pms.reset()
    pml.reset()
    # pml1.reset()
        
if __name__ == "__main__":
    main()
