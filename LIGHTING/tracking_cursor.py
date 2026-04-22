from misc_codes.equipment_settings import *
from misc_codes.general_settings import *
EQUIPMENT_FUNCTIONS().SCOPE().STOP()



for i in np.arange(0, 40e-3, 0.01e-3):
    scope.cursor(channel=1, cursor_set=1, X1=i, X2=i, Y1=0, Y2=0, type='PAIR')
    # sleep(0.05)
    # print(i)
    result = scope.get_cursor(1)
    print(float(result['y1 position'])*1000)
