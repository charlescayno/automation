from tarfile import SUPPORTED_TYPES
import pat_tool.pat_tool as pat_tool
import time

from enum import Enum

from misc_functions.misc_functions import RepeatedTimer
from dll.SLABHIDtoSMBUS import HidSmbusError
import dll
from pd.pd_types import PDO_SUPPLY_TYPE

from PySide2 import QtGui
from PySide2.QtGui import QValidator, QIntValidator, QDoubleValidator

from powi.equipment import ACSource, PowerMeter


class MANUAL_CONTROL_SETTINGS(Enum):
    POWERMETER_UPDATE_INTERVAL_S = 0.500
    USBPD_UPDATE_INTERVAL_S = 2


class USBPDSINK_STATE(Enum):
    PAT_TOOL_DISCONNECTED = 0
    PAT_TOOL_CONNECTED = 1
    USBPD_SOURCE_CONNECTED = 2

class EQUIPMENT_ADDR():
    PM_SOURCE = 2
    PM_LOAD = 30
    E_LOAD = 8

# Handles the logic for the Manual Equipment Control page
class ManualControlHandler():
    def __init__(self, parent):

        # Get a link from the parent
        self.parent = parent

        # Let the handler control the ui
        self.ui = parent.ui



        # Link UI buttons to controls
        self.ui.btn_usbpdsink_request.clicked.connect(self.pdo_request)

        # Link Request Parameter change to listwidget update
        self.ui.list_usbpdsink_sourcecaps.currentItemChanged.connect(self.request_params_text_update)
        
    def start_manual_control_handler(self):
        

        # Setup input limiting
        param1_validator = QtGui.QIntValidator()
        param1_validator.setRange(3300, 21000)
        self.ui.lineedit_manual_usbpd_request_param1.setValidator(param1_validator)

        param2_validator = QtGui.QIntValidator()
        param2_validator.setRange(1000, 3000)
        self.ui.lineedit_manual_usbpd_request_param2.setValidator(param2_validator)

        # Equipment objects
        self.initialize_usbpd()
        self.initialize_power_meter()

        # GPIB

        # USBPD
        
        # LAN for Scope


    ########################################################################
    #                          USBPD Functions START                       #
    ########################################################################
    
    def initialize_usbpd(self):
        if not self.parent.usb_initialized:
            # TODO: Remove list items on GUI file later. For now, clear in software
            self.ui.list_usbpdsink_sourcecaps.clear()
            
            
            # Instance of the SMBUS interface through CP2112
            self.smbus = pat_tool.CP2112()

            # If PAT tool connection is successful during initialization
            # Set the state to connected
            self.usbpd_state = USBPDSINK_STATE.PAT_TOOL_DISCONNECTED
            if self.smbus.connection_ok:
                        self.usbpd_state = USBPDSINK_STATE.PAT_TOOL_CONNECTED

            # Create a USBPD sink controller object
            self.usbpd_sink = pat_tool.PDSinkController()

            # Add the PD controller to the devices connected to the SMBUS
            self.smbus.add_PDController(self.usbpd_sink)

            # Flag to check if source caps need update
            self.source_caps_listed = False
            


            self.usb_periodic_update_thread = RepeatedTimer(
            interval = MANUAL_CONTROL_SETTINGS.USBPD_UPDATE_INTERVAL_S.value,
            function = self.usbpd_update)

            self.parent.usb_initialized = True
        

    def usbpd_update(self):
        pass
        # match self.usbpd_state:
        #     case USBPDSINK_STATE.PAT_TOOL_DISCONNECTED:
        #         self.try_connect_pat_tool()
                
                
        #         if self.smbus.connection_ok:
        #             self.usbpd_state = USBPDSINK_STATE.PAT_TOOL_CONNECTED

        #     case USBPDSINK_STATE.PAT_TOOL_CONNECTED:
        #         # Check if pat tool is still connected
                
        #         # Check connection to USBPD source
        #         if self.source_caps_listed == False:
        #             self.try_get_source_caps()
        #             self.source_caps_listed = True

        #         # If connection is OK, display the source caps on the list widget
        #         # if self.usbpd_sink.connection_ok:
        #         #     self.display_sourcecaps_to_listwidget()
    

        #     case USBPDSINK_STATE.USBPD_SOURCE_CONNECTED:
        #         pass

    def try_connect_pat_tool(self):
        if not self.smbus.IsOpened():
            self.smbus.open()
            self.smbus.connection_ok = True
        else:
            print("Another process is using the USB device.")
        
        self.smbus.connection_ok 
    
     
    def try_get_source_caps(self):
        try:
            self.usbpd_sink.get_source_caps()
        except IndexError:
            # TODO: Check for VBUS to have more info before sending log
            print("Please verify USB PD connection. PSU may also be turned off")
            self.usbpd_sink.connection_ok = False
        # except :
        #     print("Please check PAT tool connection")
        #     self.usbpd_sink.connection_ok = False
        else:
            self.usbpd_sink.connection_ok = True



        if self.usbpd_sink.connection_ok:
            # Update list widget
            self.ui.list_usbpdsink_sourcecaps.clear()
            for source_cap in self.usbpd_sink.pdo_list:
                self.ui.list_usbpdsink_sourcecaps.addItem(source_cap.text)
        else:
            self.ui.list_usbpdsink_sourcecaps.clear()
            self.source_caps_listed = False
            # Remove list widget items

    
    def pdo_request(self):
        # TODO: Checking of inputs
        # Get index of selected PDO
        list_widget_row = self.ui.list_usbpdsink_sourcecaps.currentRow()
        
        # If no PDO is selected, exit function
        if list_widget_row == None:
            return

        # Set object position
        object_position = list_widget_row + 1

        # Check if PDO is Fixed or Augmented
        pdo_supply_type = self.usbpd_sink.pdo_list[object_position-1].supply_type

        if pdo_supply_type == PDO_SUPPLY_TYPE.FIXED.value:
            ilim_text_input = self.ui.lineedit_manual_usbpd_request_param2.text()
            ilim_request = int(ilim_text_input)
            self.usbpd_sink.fixed_pdo_request(iout=ilim_request, object_position=object_position)
        elif pdo_supply_type == PDO_SUPPLY_TYPE.AUGMENTED.value:
            vout_text_input = self.ui.lineedit_manual_usbpd_request_param1.text()
            ilim_text_input = self.ui.lineedit_manual_usbpd_request_param2.text()

            vout_request = int(vout_text_input)/1000
            ilim_request = int(ilim_text_input)/1000
            self.usbpd_sink.pps_request(vout=vout_request, iout=ilim_request)



    ####################################
    #       UI Updates
    ####################################
    def request_params_text_update(self):
        # Get index of currently selected PDO
        list_widget_selected_row = self.ui.list_usbpdsink_sourcecaps.currentRow()
        selected_pdo = self.usbpd_sink.pdo_list[list_widget_selected_row]
        
        # If none is selected, just end function
        if list_widget_selected_row == None:
            return


        # If PDO is fixed, Change label to max current
        # Set text boxes values to PDO max current 
        if selected_pdo.supply_type == PDO_SUPPLY_TYPE.FIXED.value:
            self.ui.label_usbpdsink_request_param1.setText("Maximum Current (mA)")
            
            max_current_string = str(selected_pdo.max_current)
            self.ui.lineedit_manual_usbpd_request_param1.setText(max_current_string)
            self.ui.lineedit_manual_usbpd_request_param2.setText(max_current_string)
            
        # If PDO is augmented, change label to max voltage
        # Set text boxes to max voltage and max pps current
        elif selected_pdo.supply_type == PDO_SUPPLY_TYPE.AUGMENTED.value:
            self.ui.label_usbpdsink_request_param1.setText("Output Voltage (mV)")
            
            max_voltage_string = str(selected_pdo.max_voltage)
            self.ui.lineedit_manual_usbpd_request_param1.setText(max_voltage_string)
            
            max_current_string = str(selected_pdo.max_current)
            self.ui.lineedit_manual_usbpd_request_param2.setText(max_current_string)
        
    
    ########################################################################
    #                          USBPD Functions END                         #
    ########################################################################


    
    ########################################################################
    #                          Power Meter Functions Start                 #
    ########################################################################
    from equipment import PowerMeter, ACSource
    def initialize_power_meter(self):
        self.pm_source = PowerMeter(EQUIPMENT_ADDR.PM_SOURCE)
        self.pm_load = PowerMeter(EQUIPMENT_ADDR.PM_LOAD)

        self.powermeter_periodic_update_thread = RepeatedTimer(
        interval = MANUAL_CONTROL_SETTINGS.POWERMETER_UPDATE_INTERVAL_S.value,
        function = self.power_meter_update
        )
    
    def power_meter_update(self):

        # Source power meter display
        self.ui.label_pms_display_a.setText(f'{str(self.pm_source.voltage)} V')
        self.ui.label_pms_display_b.setText(f'{str(self.pm_source.current)} A')
        self.ui.label_pms_display_c.setText(f'{str(self.pm_source.power)} W')
        self.ui.label_pms_display_d.setText(f'{str(self.pm_source.pf)}  ')


        # Load power meter display
        self.ui.label_pml_display_a.setText(f'{str(self.pm_load.voltage)} V')
        self.ui.label_pml_display_b.setText(f'{str(self.pm_load.current)} A')
        self.ui.label_pml_display_c.setText(f'{str(self.pm_load.power)} W')
        self.ui.label_pml_display_d.setText(f'{str(self.pm_load.pf)}  ')

    def power_meter_cleanup(self):
        self.powermeter_periodic_update_thread.stop()
