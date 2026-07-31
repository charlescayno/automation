from basicgui import Ui_Form
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from PyQt5 import QtWidgets as qtw


# November 21, 2021

"""IMPORT DEPENDENCIES"""
from time import time, sleep
import sys
import os
import math
from powi.equipment import ACSource, PowerMeter, ElectronicLoad, Oscilloscope, LEDControl
from powi.equipment import headers, create_folder, footers, waveform_counter, soak, convert_argv_to_int_list, tts, prompt, sfx
from filemanager import path_maker, remove_file, move_file
import winsound as ws
from playsound import playsound
waveform_counter = 0



"""COMMS"""
ac_source_address = 5
source_power_meter_address = 1 
load_power_meter_address = 2
eload_address = 8
scope_address = "10.125.10.184"







class functionality(qtw.QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setFixedSize(862,736)
        title = "Equipment Interface"
        self.setWindowTitle(title)

        # self.set_address()

        # self.ac = ACSource(ac_source_address)
        # self.pms = PowerMeter(source_power_meter_address)
        # self.pml = PowerMeter(load_power_meter_address)
        # self.eload = ElectronicLoad(eload_address)
        self.scope = Oscilloscope(scope_address)
        # self.led = LEDControl()



        self.ui.ac_on_button.clicked.connect(self.ac_on)
        self.ui.ac_off_button.clicked.connect(self.ac_off)
        self.ui.vac_90_button.clicked.connect(self.set_vin_90)
        self.ui.vac_100_button.clicked.connect(self.set_vin_100)
        self.ui.vac_115_button.clicked.connect(self.set_vin_115)
        self.ui.vac_230_button.clicked.connect(self.set_vin_230)
        self.ui.vac_265_button.clicked.connect(self.set_vin_265)
        self.ui.vac_277_button.clicked.connect(self.set_vin_277)
        self.ui.vac_300_button.clicked.connect(self.set_vin_300)
        self.ui.vac_110_button.clicked.connect(self.set_vin_110)
        self.ui.vac_120_button.clicked.connect(self.set_vin_120)
        self.ui.vac_132_button.clicked.connect(self.set_vin_132)
        self.ui.vac_180_button.clicked.connect(self.set_vin_180)
        self.ui.vac_200_button.clicked.connect(self.set_vin_200)

        self.ui.led_load_46V_button.clicked.connect(self.set_led_load_46V)
        self.ui.led_load_36V_button.clicked.connect(self.set_led_load_36V)
        self.ui.led_load_24V_button.clicked.connect(self.set_led_load_24V)
        self.ui.led_load_NL_button.clicked.connect(self.set_led_load_NL)

        self.ui.discharge_output_button.clicked.connect(self.discharge_output)

        self.ui.scope_single_button.clicked.connect(self.scope_single)
        self.ui.scope_run_button.clicked.connect(self.scope_run)
        self.ui.scope_stop_button.clicked.connect(self.scope_stop)

        self.ui.screenshot_button.clicked.connect(self.screenshot)
        self.ss_counter = 0

        self.ui.set_scope_trigger_button.clicked.connect(self.set_trigger)
        self.ui.set_scope_horizontal_settings_button.clicked.connect(self.set_horizontal_settings)

        self.ui.ch_set_scope_settings_button.clicked.connect(self.ch1_settings)
        self.ui.ch_set_scope_settings_button_2.clicked.connect(self.ch2_settings)
        self.ui.ch_set_scope_settings_button_3.clicked.connect(self.ch3_settings)
        self.ui.ch_set_scope_settings_button_4.clicked.connect(self.ch4_settings)

        self.ui.autozero_button.clicked.connect(self.ch1_autozero)
        self.ui.autozero_button_2.clicked.connect(self.ch2_autozero)
        self.ui.autozero_button_3.clicked.connect(self.ch3_autozero)
        self.ui.autozero_button_4.clicked.connect(self.ch4_autozero)

        self.ui.auto_button.clicked.connect(self.scope_auto)
        self.ui.norm_button.clicked.connect(self.scope_norm)

        self.ui.time_position_textbox.textChanged.connect(self.change_time_position)
        self.ui.time_scale_textbox.textChanged.connect(self.change_time_scale)


    def change_time_position(self):
        self.time_position = self.ui.time_position_textbox.text()
        print(f'Time Position: {self.time_position} %')
        self.scope.time_position(self.time_position)

    def change_time_scale(self):
        self.time_scale = self.ui.time_scale_textbox.text()
        print(f'Time Scale: {self.time_scale} s / div.')
        self.scope.time_scale(self.time_scale)


    def set_vin_90(self): self.ui.ac_input_voltage_textbox.setText(str(90))
    def set_vin_100(self): self.ui.ac_input_voltage_textbox.setText(str(100))
    def set_vin_115(self): self.ui.ac_input_voltage_textbox.setText(str(115))
    def set_vin_230(self): self.ui.ac_input_voltage_textbox.setText(str(230))
    def set_vin_265(self): self.ui.ac_input_voltage_textbox.setText(str(265))
    def set_vin_277(self): self.ui.ac_input_voltage_textbox.setText(str(277))
    def set_vin_300(self): self.ui.ac_input_voltage_textbox.setText(str(300))
    def set_vin_110(self): self.ui.ac_input_voltage_textbox.setText(str(110))
    def set_vin_120(self): self.ui.ac_input_voltage_textbox.setText(str(120))
    def set_vin_132(self): self.ui.ac_input_voltage_textbox.setText(str(132))
    def set_vin_180(self): self.ui.ac_input_voltage_textbox.setText(str(180))
    def set_vin_200(self): self.ui.ac_input_voltage_textbox.setText(str(200))

    def ch1_settings(self):

        ch1_status = self.ui.ch_status_combobox.currentText()

        if ch1_status == 'ON':
            print("CH1 is ON.")

            """Time Scale"""
            try:
                self.ch1_scale = float(self.ui.ch_scale_textbox.text())
            except:
                self.ui.ch_scale_textbox.setText('1')
                self.ch1_scale = 1
            
            """Time Position"""
            try:
                self.ch1_position = float(self.ui.ch_position_textbox.text())
            except:
                self.ui.ch_position_textbox.setText('-4')
                self.ch1_position = -4
            
            """Channel Offset"""
            try:
                self.ch1_offset = float(self.ui.ch_offset_textbox.text())
            except:
                self.ui.ch_offset_textbox.setText('0')
                self.ch1_offset = 0
            
            "Label Rel X Position"
            try:
                self.ch1_rel_x = float(self.ui.ch_rel_x_textbox.text())
            except:
                self.ui.ch_rel_x_textbox.setText('20')
                self.ch1_rel_x = 20
            
            self.ch1_label = self.ui.ch_label_textbox.text()
            self.ch1_color = self.ui.ch_color_combobox.currentText()
            self.ch1_bandwidth = int(self.ui.ch_bandwidth_combobox.currentText())
            self.ch1_coupling = self.ui.ch_coupling_combobox.currentText()

            print(f'label:     {self.ch1_label}')
            print(f'scale:     {self.ch1_scale} unit/div')
            print(f'position:  {self.ch1_position} div')
            print(f'bandwidth: {self.ch1_bandwidth}')
            print(f'color:     {self.ch1_color}')
            print(f'coupling:  {self.ch1_coupling}')
            print(f'offset:    {self.ch1_offset} units')
            print(f'rel_x:     {self.ch1_rel_x} %')
            print()

            self.scope.channel_settings(ch1_status, 1, self.ch1_scale, self.ch1_position, self.ch1_label, self.ch1_color, self.ch1_rel_x, self.ch1_bandwidth, self.ch1_coupling, self.ch1_offset)

            
        else:
            print("CH1 is OFF.\n")
            self.scope.channel_settings('OFF', channel=1)

    def ch2_settings(self):

        ch2_status = self.ui.ch_status_combobox_2.currentText()

        if ch2_status == 'ON':
            print("CH2 is ON.")

            """Time Scale"""
            try:
                self.ch2_scale = float(self.ui.ch_scale_textbox_2.text())
            except:
                self.ui.ch_scale_textbox_2.setText('1')
                self.ch2_scale = 1
            
            """Time Position"""
            try:
                self.ch2_position = float(self.ui.ch_position_textbox_2.text())
            except:
                self.ui.ch_position_textbox_2.setText('-4')
                self.ch2_position = -4
            
            """Channel Offset"""
            try:
                self.ch2_offset = float(self.ui.ch_offset_textbox_2.text())
            except:
                self.ui.ch_offset_textbox_2.setText('0')
                self.ch2_offset = 0

            "Label Rel X Position"
            try:
                self.ch2_rel_x = float(self.ui.ch_rel_x_textbox_2.text())
            except:
                self.ui.ch_rel_x_textbox_2.setText('40')
                self.ch2_rel_x = 40
            
            self.ch2_label = self.ui.ch_label_textbox_2.text()
            self.ch2_color = self.ui.ch_color_combobox_2.currentText()
            self.ch2_bandwidth = int(self.ui.ch_bandwidth_combobox_2.currentText())
            self.ch2_coupling = self.ui.ch_coupling_combobox_2.currentText()
            

            print(f'label:     {self.ch2_label}')
            print(f'scale:     {self.ch2_scale} unit/div')
            print(f'position:  {self.ch2_position} div')
            print(f'bandwidth: {self.ch2_bandwidth}')
            print(f'color:     {self.ch2_color}')
            print(f'coupling:  {self.ch2_coupling}')
            print(f'offset:    {self.ch2_offset} units')
            print(f'rel_x:     {self.ch2_rel_x} %')
            print()

            self.scope.channel_settings(ch2_status, 2, self.ch2_scale, self.ch2_position, self.ch2_label, self.ch2_color, self.ch2_rel_x, self.ch2_bandwidth, self.ch2_coupling, self.ch2_offset)

            
        else:
            print("CH2 is OFF.\n")
            self.scope.channel_settings('OFF', channel=2)

    def ch3_settings(self):

        ch3_status = self.ui.ch_status_combobox_3.currentText()

        if ch3_status == 'ON':
            print("CH3 is ON.")

            """Time Scale"""
            try:
                self.ch3_scale = float(self.ui.ch_scale_textbox_3.text())
            except:
                self.ui.ch_scale_textbox_3.setText('1')
                self.ch3_scale = 1
            
            """Time Position"""
            try:
                self.ch3_position = float(self.ui.ch_position_textbox_3.text())
            except:
                self.ui.ch_position_textbox_3.setText('-4')
                self.ch3_position = -4
            
            """Channel Offset"""
            try:
                self.ch3_offset = float(self.ui.ch_offset_textbox_3.text())
            except:
                self.ui.ch_offset_textbox_3.setText('0')
                self.ch3_offset = 0

            "Label Rel X Position"
            try:
                self.ch3_rel_x = float(self.ui.ch_rel_x_textbox_3.text())
            except:
                self.ui.ch_rel_x_textbox_3.setText('40')
                self.ch3_rel_x = 40
            
            self.ch3_label = self.ui.ch_label_textbox_3.text()
            self.ch3_color = self.ui.ch_color_combobox_3.currentText()
            self.ch3_bandwidth = int(self.ui.ch_bandwidth_combobox_3.currentText())
            self.ch3_coupling = self.ui.ch_coupling_combobox_3.currentText()
            

            print(f'label:     {self.ch3_label}')
            print(f'scale:     {self.ch3_scale} unit/div')
            print(f'position:  {self.ch3_position} div')
            print(f'bandwidth: {self.ch3_bandwidth}')
            print(f'color:     {self.ch3_color}')
            print(f'coupling:  {self.ch3_coupling}')
            print(f'offset:    {self.ch3_offset} units')
            print(f'rel_x:     {self.ch3_rel_x} %')
            print()

            self.scope.channel_settings(ch3_status, 3, self.ch3_scale, self.ch3_position, self.ch3_label, self.ch3_color, self.ch3_rel_x, self.ch3_bandwidth, self.ch3_coupling, self.ch3_offset)

            
        else:
            print("CH3 is OFF.\n")
            self.scope.channel_settings('OFF', channel=3)
    
    def ch4_settings(self):

        ch4_status = self.ui.ch_status_combobox_4.currentText()

        if ch4_status == 'ON':
            print("CH4 is ON.")

            """Time Scale"""
            try:
                self.ch4_scale = float(self.ui.ch_scale_textbox_4.text())
            except:
                self.ui.ch_scale_textbox_4.setText('1')
                self.ch4_scale = 1
            
            """Time Position"""
            try:
                self.ch4_position = float(self.ui.ch_position_textbox_4.text())
            except:
                self.ui.ch_position_textbox_4.setText('-4')
                self.ch4_position = -4
            
            """Channel Offset"""
            try:
                self.ch4_offset = float(self.ui.ch_offset_textbox_4.text())
            except:
                self.ui.ch_offset_textbox_4.setText('0')
                self.ch4_offset = 0

            "Label Rel X Position"
            try:
                self.ch4_rel_x = float(self.ui.ch_rel_x_textbox_4.text())
            except:
                self.ui.ch_rel_x_textbox_4.setText('40')
                self.ch4_rel_x = 40
            
            self.ch4_label = self.ui.ch_label_textbox_4.text()
            self.ch4_color = self.ui.ch_color_combobox_4.currentText()
            self.ch4_bandwidth = int(self.ui.ch_bandwidth_combobox_4.currentText())
            self.ch4_coupling = self.ui.ch_coupling_combobox_4.currentText()
            

            print(f'label:     {self.ch4_label}')
            print(f'scale:     {self.ch4_scale} unit/div')
            print(f'position:  {self.ch4_position} div')
            print(f'bandwidth: {self.ch4_bandwidth}')
            print(f'color:     {self.ch4_color}')
            print(f'coupling:  {self.ch4_coupling}')
            print(f'offset:    {self.ch4_offset} units')
            print(f'rel_x:     {self.ch4_rel_x} %')
            print()

            self.scope.channel_settings(ch4_status, 4, self.ch4_scale, self.ch4_position, self.ch4_label, self.ch4_color, self.ch4_rel_x, self.ch4_bandwidth, self.ch4_coupling, self.ch4_offset)

            
        else:
            print("CH4 is OFF.\n")
            self.scope.channel_settings('OFF', channel=4)

    def set_horizontal_settings(self):

        if self.ui.time_position_textbox.text().isnumeric() == False:
            print("Invalid input")
            self.ui.time_position_textbox.setText('50')
            self.time_position = 50
        else:
            self.time_position = float(self.ui.time_position_textbox.text())

        try:
            self.time_scale = float(self.ui.time_scale_textbox.text())
        except ValueError:
            print("Invalid input. Set to default value.")
            self.ui.time_scale_textbox.setText('0.1')
            self.time_scale = 0.1

        print(f'time_position: {self.time_position} %')
        print(f'time_scale: {self.time_scale} s/div.')
        self.scope.position_scale(self.time_position, self.time_scale)
    
    def set_trigger(self):

        import re
        self.trigger_level = re.sub("[^\d\.]", "", self.ui.trigger_level_textbox.text())
        
        self.trigger_channel = int(self.ui.trigger_channel_combobox.currentText())

        self.trigger_edge = self.ui.trigger_edge_combobox.currentText()

        print(f'Trigger: {self.trigger_level} {self.trigger_edge} at channel {self.trigger_channel}')

        self.scope.edge_trigger(self.trigger_channel, self.trigger_level, self.trigger_edge)

    def screenshot(self):

        # self.scope.stop()

        self.filename = self.ui.filename_textbox.text()
        if self.ui.filename_textbox.text() == '': self.filename = 'default'
        
        if self.ss_counter == 0: self.original_filename = self.filename
        elif self.ui.filename_textbox.text() != f'{self.original_filename}_{self.ss_counter}':
            self.ss_counter = 0
            self.original_filename = self.filename

        if self.ui.folder_path_textbox.text() == '': self.path = f"C:/Users/ccayno/Desktop/Oscilloscope/"
        else: self.path = self.ui.folder_path_textbox.text()
        
        
        

        print(f'{self.filename} >> {self.path}')
        self.ss_file = self.filename + '.png'
        self.scope.get_screenshot(self.ss_file, self.path)

        # if self.filename == 'default':
        #     self.ss_counter += 1
        #     self.ui.filename_textbox.setText(f'default_{self.ss_counter}')
        # elif self.ui.filename_textbox.text() == f'{self.original_filename}':
        #     self.ss_counter += 1
        #     self.ui.filename_textbox.setText(f'{self.original_filename}_{self.ss_counter}')
        # elif self.ui.filename_textbox.text() == f'{self.original_filename}_{self.ss_counter}':
        #     self.ss_counter += 1
        #     self.ui.filename_textbox.setText(f'{self.original_filename}_{self.ss_counter}')
        # else: 
        #     self.ss_counter = 0

    def scope_auto(self):
        print("Trigger Mode: AUTO")
        self.scope.trigger_mode('AUTO')

    def scope_norm(self):
        print("Trigger Mode: NORM")
        self.scope.trigger_mode('NORM')

    def scope_single(self):
        print("Run Single.")
        
        # if self.ui.filename_textbox.text() == f'' or self.ui.filename_textbox.text() == f'Startup':  
        #     self.ui.filename_textbox.setText(f'Startup')
        # elif self.ui.filename_textbox.text() == 'NL' or self.ui.filename_textbox.text() == 'NL, Startup':  
        #     self.ui.filename_textbox.setText(f'NL, Startup')
        # elif self.ui.filename_textbox.text() == f'{self.led_voltage}V' or self.ui.filename_textbox.text() == f'{self.led_voltage}V, Startup':
        #     self.ui.filename_textbox.setText(f'{self.led_voltage}V, Startup')
        # elif self.ui.filename_textbox.text() == f'{self.vin}Vac':
        #     self.ui.filename_textbox.setText(f'{self.vin}Vac, Normal')
        # elif self.ui.filename_textbox.text() == f'{self.led_voltage}V, {self.vin}Vac':
        #     self.ui.filename_textbox.setText(f'{self.led_voltage}V, {self.vin}Vac, Normal')
        
        self.scope.run_single()
    
    def scope_run(self):
        print("Run Normal.")

        self.scope.run()
    
    def scope_stop(self):
        print("Run Stop.")
        self.scope.stop()

    def discharge_output(self):
        # self.pms.write(':INTEGrate:RESet')
        print("Discharging output.")
        self.ui.filename_textbox.setText('')
        self.ac.turn_off()
        for i in range(1,9):
            self.eload.channel[i].cc = 1
            self.eload.channel[i].turn_on()
            self.eload.channel[i].short_on()
        sleep(0.5)
        for i in range(1,9):
            self.eload.channel[i].turn_off()
            self.eload.channel[i].short_off()
        sleep(0.5)

    def ac_on(self):

        if self.ui.ac_input_voltage_textbox.text().isnumeric() == False:
            print("Invalid input")
            self.ui.ac_input_voltage_textbox.setText('0')
            self.vin = 0
        else:
            self.vin = int(self.ui.ac_input_voltage_textbox.text())
            if self.vin > 300:
                self.vin = 300
                self.ui.ac_input_voltage_textbox.setText('300')

        
        # if self.ui.filename_textbox.text() == '':
        #     self.set_led_load_46V()
        #     self.ui.filename_textbox.setText(f'{self.led_voltage}V, {self.vin}Vac, Normal')
        # elif self.ui.filename_textbox.text() == 'NL':
        #     self.ui.filename_textbox.setText(f'NL, {self.vin}Vac, Normal')
        # elif self.ui.filename_textbox.text() == f'{self.led_voltage}V':
        #     self.ui.filename_textbox.setText(f'{self.led_voltage}V, {self.vin}Vac, Normal')
        # elif self.ui.filename_textbox.text() == f'Startup':
        #     self.set_led_load_46V()
        #     self.ui.filename_textbox.setText(f'{self.led_voltage}V, {self.vin}Vac, Startup')
        # elif self.ui.filename_textbox.text() == f'NL, Startup':
        #     self.ui.filename_textbox.setText(f'NL, {self.vin}Vac, Startup')
        # elif self.ui.filename_textbox.text() == f'{self.led_voltage}V, Startup':
        #     self.ui.filename_textbox.setText(f'{self.led_voltage}V, {self.vin}Vac, Startup')
        # elif self.ui.filename_textbox.text() == f'{self.led_voltage}V':
        #     self.ui.filename_textbox.setText(f'{self.led_voltage}V, {self.vin}Vac')    
        # elif self.ui.filename_textbox.text() == 'NL':
        #     self.ui.filename_textbox.setText(f'NL, {self.vin}Vac')
        
        self.ac.voltage = self.vin
        self.ac.turn_on()
        print(f"AC ON: {self.vin}Vac")

    def ac_off(self):
        print("AC OFF")
        self.ac.turn_off()
        self.ui.filename_textbox.setText('')
    
    def ch1_autozero(self):
        print(f"Auto Zero at CH1")
        self.scope.auto_zero(1)
    
    def ch2_autozero(self):
        print(f"Auto Zero at CH2")
        self.scope.auto_zero(2)

    def ch3_autozero(self):
        print(f"Auto Zero at CH3")
        self.scope.auto_zero(3)

    def ch4_autozero(self):
        print(f"Auto Zero at CH4")
        self.scope.auto_zero(4)
    


    def set_led_load_46V(self):
        print("Set LED load to 46V")
        self.led_voltage = 46


        # if self.ui.filename_textbox.text() == f'':  
        #     self.ui.filename_textbox.setText(f'{self.led_voltage}V')
        # elif self.ui.filename_textbox.text() == f'46V' or self.ui.filename_textbox.text() == f'36V' or self.ui.filename_textbox.text() == f'24V' or self.ui.filename_textbox.text() == f'NL':  
        #     self.ui.filename_textbox.setText(f'{self.led_voltage}V')
        # elif self.ui.filename_textbox.text() == f'46V, Startup' or self.ui.filename_textbox.text() == f'36V, Startup' or self.ui.filename_textbox.text() == f'24V, Startup' or self.ui.filename_textbox.text() == f'NL, Startup':
        #     self.ui.filename_textbox.setText(f'{self.led_voltage}V, Startup')
        # elif self.ui.filename_textbox.text() == f'Startup':
        #     self.ui.filename_textbox.setText(f'{self.led_voltage}V, Startup')
        # elif self.ui.filename_textbox.text() == f'{self.vin}Vac':
        #     self.ui.filename_textbox.setText(f'{self.led_voltage}V, {self.vin}Vac')
        
        self.led.voltage(self.led_voltage)
    
    def set_led_load_36V(self):
        print("Set LED load to 36V")
        self.led_voltage = 36
        
        # if self.ui.filename_textbox.text() == f'':  
        #     self.ui.filename_textbox.setText(f'{self.led_voltage}V')
        # elif self.ui.filename_textbox.text() == f'46V' or self.ui.filename_textbox.text() == f'36V' or self.ui.filename_textbox.text() == f'24V' or self.ui.filename_textbox.text() == f'NL':
        #     self.ui.filename_textbox.setText(f'{self.led_voltage}V')
        # elif self.ui.filename_textbox.text() == f'46V, Startup' or self.ui.filename_textbox.text() == f'36V, Startup' or self.ui.filename_textbox.text() == f'24V, Startup' or self.ui.filename_textbox.text() == f'NL, Startup':
        #     self.ui.filename_textbox.setText(f'{self.led_voltage}V, Startup')
        # elif self.ui.filename_textbox.text() == f'Startup':
        #     self.ui.filename_textbox.setText(f'{self.led_voltage}V, Startup')
        # elif self.ui.filename_textbox.text() == f'{self.vin}Vac':
        #     self.ui.filename_textbox.setText(f'{self.led_voltage}V, {self.vin}Vac')
        
        self.led.voltage(self.led_voltage)
    
    def set_led_load_24V(self):
        print("Set LED load to 24V")
        self.led_voltage = 24
        
        # if self.ui.filename_textbox.text() == f'':  
        #     self.ui.filename_textbox.setText(f'{self.led_voltage}V')
        # elif self.ui.filename_textbox.text() == f'46V' or self.ui.filename_textbox.text() == f'36V' or self.ui.filename_textbox.text() == f'24V' or self.ui.filename_textbox.text() == f'NL':
        #     self.ui.filename_textbox.setText(f'{self.led_voltage}V')
        # elif self.ui.filename_textbox.text() == f'46V, Startup' or self.ui.filename_textbox.text() == f'36V, Startup' or self.ui.filename_textbox.text() == f'24V, Startup' or self.ui.filename_textbox.text() == f'NL, Startup':
        #     self.ui.filename_textbox.setText(f'{self.led_voltage}V, Startup')
        # elif self.ui.filename_textbox.text() == f'Startup':
        #     self.ui.filename_textbox.setText(f'{self.led_voltage}V, Startup')
        # elif self.ui.filename_textbox.text() == f'{self.vin}Vac':
        #     self.ui.filename_textbox.setText(f'{self.led_voltage}V, {self.vin}Vac')
        
        self.led.voltage(self.led_voltage)
    
    def set_led_load_NL(self):
        print("Set LED load to NL")
        self.led_voltage = 0
        
        # if self.ui.filename_textbox.text() == f'':  
        #     self.ui.filename_textbox.setText(f'NL')
        # elif self.ui.filename_textbox.text() == f'46V' or self.ui.filename_textbox.text() == f'36V' or self.ui.filename_textbox.text() == f'24V' or self.ui.filename_textbox.text() == f'NL': 
        #     self.ui.filename_textbox.setText(f'NL')
        # elif self.ui.filename_textbox.text() == f'46V, Startup' or self.ui.filename_textbox.text() == f'36V, Startup' or self.ui.filename_textbox.text() == f'24V, Startup' or self.ui.filename_textbox.text() == f'NL, Startup':
        #     self.ui.filename_textbox.setText(f'NL, Startup')
        # elif self.ui.filename_textbox.text() == f'Startup':
        #     self.ui.filename_textbox.setText(f'NL, Startup')
        # elif self.ui.filename_textbox.text() == f'{self.vin}Vac':
        #     self.ui.filename_textbox.setText(f'NL, {self.vin}Vac')
        
        self.led.voltage(self.led_voltage)


if __name__ == '__main__':
    app = qtw.QApplication([])

    widget = functionality()
    widget.show()

    app.exec()

