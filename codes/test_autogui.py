
from AUTOGUI_CONFIG import *
from time import sleep

ate_gui = AutoguiCalibrate()
# input()
# coords = ate_gui.load_coordinates()
# pyautogui.moveTo(coords['AC_ON'])
# ate_gui.recalibrate()
ate_gui.alt_tab()
# ate_gui.moveTo('AC_ON')
# ate_gui.click('AC_ON')
ate_gui.click('INITIALIZE_COM_PORT')
# sleep(5)
ate_gui.change_rheostat_settings(10, 10, 1)

# input()


# input()




# from general import *

# test = Initialize()

# # address = test.load_settings()
# # print(address)
# # test.recalibrate()
# # print(test.load_settings())

# test.Equipment()