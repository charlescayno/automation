from powi.MULTIPROTOCOL_CONTROL import MultiprotocolControl
control = MultiprotocolControl()

import sys

while True:
    voltage = float(input("Enter voltage: "))
    print(f"{voltage} V")
    control.manual_set_analog(voltage)
    input()