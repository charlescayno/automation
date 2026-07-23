from misc_codes.equipment_settings import *
from misc_codes.general_settings import *
from battery_discharge import main_battery_discharge

def main():
    # ac.reset()
    pms.reset()
    pml.reset()
    
if __name__ == "__main__":
    main()
    print("Power meters has been reset")
