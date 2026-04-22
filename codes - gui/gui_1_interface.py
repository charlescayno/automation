from re import L
from gui_3 import Ui_MainWindow
from meas1 import Ui_Form


from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from PyQt5 import QtWidgets as qtw

import qdarkgraystyle


##################################################################################
"""IMPORT DEPENDENCIES"""
from time import time, sleep
import sys
import os
import math
import numpy as np
import shutil
import os
import pandas as pd
import re

# from powi.equipment import ACSource, PowerMeter, ElectronicLoad, Oscilloscope, LEDControl, Keithley_DC_2230G
from powi.equipment import Oscilloscope
# from powi.equipment import headers, create_folder, footers, waveform_counter, soak, convert_argv_to_int_list, tts, prompt
# from powi.equipment import excel_to_df, df_to_excel, image_to_excel, col_row_extractor, get_anchor
# from powi.equipment import create_header_list, export_to_excel, export_screenshot_to_excel
# from powi.equipment import path_maker, remove_file

import getpass
username = getpass.getuser().lower()

from datetime import datetime
now = datetime.now()
date = now.strftime('%m%d')
##################################################################################

class MeasurementWindow1(qtw.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setFixedSize(273, 212)
        title = "Measure 1"
        self.setWindowTitle(title)

        
class MainWindow(qtw.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setFixedSize(1304, 806)
        title = "Equipment Interface"
        self.setWindowTitle(title)

        self.ui.setting.clicked.connect(self.window2)

        self.color = self.Color()

        self.ui.scope_control.setEnabled(False)
        self.ui.eload_control.setEnabled(False)
        self.ui.ac_control.setEnabled(False)
        self.ui.led_control.setEnabled(False)

        self.ui.comms_ac_button.clicked.connect(self.check_connection)
        self.ui.comms_eload_button.clicked.connect(self.check_connection)
        self.ui.comms_scope_button.clicked.connect(self.check_connection)
        self.ui.comms_led_button.clicked.connect(self.check_connection)

        self.ui.eload_enable_button.setCheckable(True)
        self.ui.eload_enable_button.clicked.connect(self.eload_enable)
        self.ui.eload_iout_label.hide()

        self.ui.scope_run_stop_button.setCheckable(True)
        self.ui.scope_run_stop_button.clicked.connect(self.scope_run_stop)

        self.ui.scope_single_button.setCheckable(True)
        self.ui.scope_single_button.clicked.connect(self.scope_run_single)

        self.ui.time_position_textbox.textChanged.connect(self.change_scope_settings)
        self.ui.time_scale_textbox.textChanged.connect(self.change_scope_settings)
        self.ui.trigger_type_combobox.currentIndexChanged.connect(self.change_scope_settings)
        self.ui.trigger_level_textbox.textChanged.connect(self.change_scope_settings)
        self.ui.trigger_channel_combobox.currentIndexChanged.connect(self.change_scope_settings)
        self.ui.trigger_edge_combobox.currentIndexChanged.connect(self.change_scope_settings)
        
        # self.ui.message.qt

    def window2(self):

        self.w = MeasurementWindow1()
        self.w.show()

    class Color:

        def lightgreen(self):
            return "background-color : #00FF7F"

        def red(self):
            return "background-color : #ff6568"

    def numeric_parser(self, string_input):
        return re.sub("[^\d\.]", "", string_input)

    def check_connection(self):
        self.button = self.sender()
        self.equipment_type = self.button.objectName().split('_')[1]
        if self.equipment_type != 'led': self.address = self.numeric_parser( getattr(self.ui, f'{self.equipment_type}_address_textbox').text() )        
        try:
            if self.equipment_type == 'ac': self.ac = ACSource(self.address)
            elif self.equipment_type == 'eload': self.eload = ElectronicLoad(self.address)
            elif self.equipment_type == 'scope':
                # self.scope = Oscilloscope(self.address)
                self.scope = Oscilloscope('10.125.10.101')
                self.scope.display_intensity()
                self.ui.scope_control.setEnabled(True)
                self.set_to_the_highest_record_length()
                # self.scope.auto_zero(2)
                self.get_scope_settings()
            else: self.led = LEDControl()
            
            self.button.setStyleSheet(self.color.lightgreen())
            self.button.setText("Connected")
            
            # getattr(self.ui, f'{self.equipment_type}_control').setEnabled(True)
        except:
            print(f'Wrong {self.equipment_type.upper()} address.')
            self.button.setStyleSheet(self.color.red())
            self.button.setText("Connection Error!")
            # getattr(self.ui, f'{self.equipment_type}_control').setEnabled(False)

    def set_to_the_highest_record_length(self):
        self.scope.record_length(10E6)
        self.scope.record_length(20E6)
        self.scope.record_length(50E6)
        self.scope.record_length(100E6)

    def change_scope_settings(self):
        self.scope.time_scale(self.ui.time_scale_textbox.text())
        self.scope.time_position(self.ui.time_position_textbox.text())
        
        if self.ui.trigger_type_combobox.currentText() == 'Edge': self.scope.edge_trigger(self.ui.trigger_channel_combobox.currentText(), self.ui.trigger_level_textbox.text(), self.ui.trigger_edge_combobox.currentText())
        if self.ui.trigger_type_combobox.currentText() == 'Window': self.scope.width_trigger(self.ui.trigger_channel_combobox.currentText(), self.ui.trigger_edge_combobox.currentText(), width_range='LONG', width=100E-3, delta=0)
        if self.ui.trigger_type_combobox.currentText() == 'Timeout': self.scope.timeout_trigger(self.ui.trigger_channel_combobox.currentText(), timeout_range='HIGH', timeout_time=1E-3)
        

    def get_scope_settings(self):
        self.ui.time_position_textbox.setText(str(self.scope.get_horizontal()['position']))
        self.ui.time_scale_textbox.setText(str(self.scope.get_horizontal()['scale']))




    def eload_enable(self):

        if self.ui.eload_enable_button.isChecked():
            self.ui.eload_enable_button.setStyleSheet(self.color.lightgreen())
        else:
            self.ui.eload_enable_button.setStyleSheet(self.color.red())

    def scope_run_stop(self):
        if self.ui.scope_run_stop_button.isChecked():
            self.ui.scope_run_stop_button.setStyleSheet(self.color.lightgreen())
            self.scope.run()
        else:
            self.ui.scope_run_stop_button.setStyleSheet(self.color.red())
            self.scope.stop()

    def scope_run_single(self):
        if self.ui.scope_single_button.isChecked():
            self.ui.scope_run_stop_button.setStyleSheet(self.color.lightgreen())
            self.scope.run_single()
        else:
            self.ui.scope_run_stop_button.setStyleSheet(self.color.red())
            self.scope.stop()

    def scope_auto(self):
        if self.ui.scope_single_button.isChecked():
            self.ui.scope_run_stop_button.setStyleSheet(self.color.lightgreen())
            self.scope.trigger_mode(mode='AUTO')
        else:
            self.ui.scope_run_stop_button.setStyleSheet(self.color.red())
            self.scope.stop()
    
    
        


if __name__ == '__main__':
    app = qtw.QApplication([])
    mainwindow = MainWindow()
    # app.setStyleSheet(qdarkgraystyle.load_stylesheet())
    mainwindow.show()
    app.exec()