################################################################################
##
## BY: WANDERSON M.PIMENTA
## PROJECT MADE WITH: Qt Designer and PySide2
## V: 1.0.0
##
## This project can be used freely for all uses, as long as they maintain the
## respective credits only in the Python scripts, any information in the visual
## interface (GUI) can be modified without any implication.
##
## There are limitations on Qt licenses if you want to use your products
## commercially, I recommend reading them on the official website:
## https://doc.qt.io/qtforpython/licenses.html
##
################################################################################

import sys
import platform
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QEvent)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PySide2.QtWidgets import *
import os

from enum import Enum

from page_controls import manual_control


# GUI FILE
from app.app_modules import *

class STACK_PAGE(Enum):
    HOME                    = 0
    EQUIPMENT_SETUP         = 1
    MANUAL_CONTROL          = 2
    ADD_TESTS               = 3
    TEST_LIST               = 4
    VIEW_LOGS               = 5
    SAVE_LOAD_CONFIG        = 6
    SETTINGS                = 7


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        ## PRINT ==> SYSTEM
        print('System: ' + platform.system())
        print('Version: ' +platform.release())

        ########################################################################
        ## START - WINDOW ATTRIBUTES
        ########################################################################

        ## REMOVE ==> STANDARD TITLE BAR
        UIFunctions.removeTitleBar(True)
        ## ==> END ##

        ## SET ==> WINDOW TITLE
        self.setWindowTitle('USBPD ATE')
        UIFunctions.labelTitle(self, 'USBPD ATE')
        UIFunctions.labelDescription(self, 'Power Integrations')
        ## ==> END ##

        ## WINDOW SIZE ==> DEFAULT SIZE
        startSize = QSize(1920, 1080)
        self.resize(startSize)
        self.setMinimumSize(startSize)
        # UIFunctions.enableMaximumSize(self, 500, 720)
        ## ==> END ##

        # TODO: Place these items in more suitable locations later
        self.previous_stackwidget_index = 0
        self.usb_initialized = False
        self.manual_control_handler = manual_control.ManualControlHandler(self)

        ## ==> CREATE MENUS
        ########################################################################

        ## ==> TOGGLE MENU SIZE
        self.ui.btn_toggle_menu.clicked.connect(lambda: UIFunctions.toggleMenu(self, 220, True))
        ## ==> END ##

        ## ==> ADD CUSTOM MENUS
        self.ui.stackedWidget.setMinimumWidth(20)
        UIFunctions.addNewMenu(self, "Home", "btn_home", "url(:/16x16/icons/16x16/cil-home.png)", True)
        UIFunctions.addNewMenu(self, "Equipment Setup", "btn_equipment_setup", "url(:/20x20/icons/20x20/cil-equalizer.png)", True)
        UIFunctions.addNewMenu(self, "Manual Control", "btn_manual_control", "url(:/20x20/icons/20x20/cil-touch-app.png)", True)
        
        UIFunctions.addNewMenu(self, "Add Tests", "btn_add_tests", "url(:/20x20/icons/20x20/cil-library-add.png)", True)
        UIFunctions.addNewMenu(self, "Test List", "btn_test_list", "url(:/20x20/icons/20x20/cil-list.png)", True)
        UIFunctions.addNewMenu(self, "View Logs", "btn_view_logs", "url(:/20x20/icons/20x20/cil-notes.png)", True)
        
        UIFunctions.addNewMenu(self, "Save/Load Configuration", "btn_save_load_configs", "url(:/20x20/icons/20x20/cil-save.png)", False)
        UIFunctions.addNewMenu(self, "Settings", "btn_settings", "url(:/20x20/icons/20x20/cil-settings.png)", False)
        
       
        ## ==> END ##

        # START MENU => SELECTION
        UIFunctions.selectStandardMenu(self, "btn_home")
        ## ==> END ##

        ## ==> START PAGE
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_home)
        ## ==> END ##

        ## STACKED WIDGET => PAGE SIGNALS
        # self.ui.stackedWidget.changeEvent.connect(self.stacked_widget_page_change)
        self.ui.stackedWidget.currentChanged.connect(self.stacked_widget_page_change)
        ## ==> END ##


        ## USER ICON ==> SHOW HIDE
        user_name = os.getlogin()[0:2]
        UIFunctions.userIcon(self, user_name, "", True)
        ## ==> END ##


        ## ==> MOVE WINDOW / MAXIMIZE / RESTORE
        ########################################################################
        def moveWindow(event):
            # IF MAXIMIZED CHANGE TO NORMAL
            if UIFunctions.returStatus() == 1:
                UIFunctions.maximize_restore(self)

            # MOVE WINDOW
            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.dragPos)
                self.dragPos = event.globalPos()
                event.accept()

        # WIDGET TO MOVE
        self.ui.frame_label_top_btns.mouseMoveEvent = moveWindow
        ## ==> END ##

        ## ==> LOAD DEFINITIONS
        ########################################################################
        UIFunctions.uiDefinitions(self)
        ## ==> END ##

        ########################################################################
        ## END - WINDOW ATTRIBUTES
        ############################## ---/--/--- ##############################




        ########################################################################
        #                                                                      #
        ## START -------------- WIDGETS FUNCTIONS/PARAMETERS ---------------- ##
        #                                                                      #
        ## ==> USER CODES BELLOW                                              ##
        ########################################################################



        ## ==> QTableWidget RARAMETERS
        ########################################################################
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        ## ==> END ##



        ########################################################################
        #                                                                      #
        ## END --------------- WIDGETS FUNCTIONS/PARAMETERS ----------------- ##
        #                                                                      #
        ############################## ---/--/--- ##############################


        ## SHOW ==> MAIN WINDOW
        ########################################################################
        # self.showMaximized()
        self.show()
        ## ==> END ##
    # Logic for page change
    def stacked_widget_page_change(self):
        current_index  = self.ui.stackedWidget.currentIndex()
        
        print(f'current_index = {current_index}, previous_index = {self.previous_stackwidget_index}')
        if self.previous_stackwidget_index == STACK_PAGE.MANUAL_CONTROL.value:
            print("End threads for manual control")

        if current_index == STACK_PAGE.MANUAL_CONTROL.value:
            print("Start threads for manual control")
            self.manual_control_handler.start_manual_control_handler()

        self.previous_stackwidget_index = current_index



    ########################################################################
    ## MENUS ==> DYNAMIC MENUS FUNCTIONS
    ########################################################################
    def Button(self):
        # GET BT CLICKED
        btnWidget = self.sender()

        # PAGE HOME
        if btnWidget.objectName() == "btn_home":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_home)
            UIFunctions.resetStyle(self, "btn_home")
            UIFunctions.labelPage(self, "Home")
            btnWidget.setStyleSheet(UIFunctions.selectMenu(btnWidget.styleSheet()))
        
        
        # PAGE EQUIPMENT SETUP
        if btnWidget.objectName() == "btn_equipment_setup":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_equipment_setup)
            UIFunctions.resetStyle(self, "btn_equipment_setup")
            UIFunctions.labelPage(self, "EQUIPMENT SETUP")
            btnWidget.setStyleSheet(UIFunctions.selectMenu(btnWidget.styleSheet()))

        # PAGE MANUAL EQUIPMENT CONTROL
        if btnWidget.objectName() == "btn_manual_control":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_manual_control)
            UIFunctions.resetStyle(self, "btn_manual_control")
            UIFunctions.labelPage(self, "Manual Equipment Control")
            btnWidget.setStyleSheet(UIFunctions.selectMenu(btnWidget.styleSheet()))

        # PAGE ADD TESTS
        if btnWidget.objectName() == "btn_add_tests":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_add_tests)
            UIFunctions.resetStyle(self, "btn_add_tests")
            UIFunctions.labelPage(self, "Add Tests")
            btnWidget.setStyleSheet(UIFunctions.selectMenu(btnWidget.styleSheet()))
        
        # PAGE TEST LIST
        if btnWidget.objectName() == "btn_test_list":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_test_list)
            UIFunctions.resetStyle(self, "btn_test_list")
            UIFunctions.labelPage(self, "Test List")
            btnWidget.setStyleSheet(UIFunctions.selectMenu(btnWidget.styleSheet()))
        
        # PAGE VIEW LOGS
        if btnWidget.objectName() == "btn_view_logs":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_view_logs)
            UIFunctions.resetStyle(self, "btn_view_logs")
            UIFunctions.labelPage(self, "View Logs")
            btnWidget.setStyleSheet(UIFunctions.selectMenu(btnWidget.styleSheet()))

        # PAGE SAVE / LOAD CONFIGS
        if btnWidget.objectName() == "btn_save_load_configs":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_save_load_configs)
            UIFunctions.resetStyle(self, "btn_save_load_configs")
            UIFunctions.labelPage(self, "Save / Load Configs")
            btnWidget.setStyleSheet(UIFunctions.selectMenu(btnWidget.styleSheet()))

        # PAGE SETTINGS
        if btnWidget.objectName() == "btn_settings":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_settings)
            UIFunctions.resetStyle(self, "btn_settings")
            UIFunctions.labelPage(self, "Settings")
            btnWidget.setStyleSheet(UIFunctions.selectMenu(btnWidget.styleSheet()))

        # PAGE WIDGETS
        if btnWidget.objectName() == "btn_widgets":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_widgets)
            UIFunctions.resetStyle(self, "btn_widgets")
            UIFunctions.labelPage(self, "Custom Widgets")
            btnWidget.setStyleSheet(UIFunctions.selectMenu(btnWidget.styleSheet()))

    ## ==> END ##

    ########################################################################
    ## START ==> APP EVENTS
    ########################################################################

    ## EVENT ==> MOUSE DOUBLE CLICK
    ########################################################################
    def eventFilter(self, watched, event):
        if watched == self.le and event.type() == QtCore.QEvent.MouseButtonDblClick:
            print("pos: ", event.pos())
    ## ==> END ##

    ## EVENT ==> MOUSE CLICK
    ########################################################################
    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()
        if event.buttons() == Qt.LeftButton:
            print('Mouse click: LEFT CLICK')
        if event.buttons() == Qt.RightButton:
            print('Mouse click: RIGHT CLICK')
        if event.buttons() == Qt.MidButton:
            print('Mouse click: MIDDLE BUTTON')
    ## ==> END ##

    ## EVENT ==> KEY PRESSED
    ########################################################################
    def keyPressEvent(self, event):
        print('Key: ' + str(event.key()) + ' | Text Press: ' + str(event.text()))
    ## ==> END ##

    ## EVENT ==> RESIZE EVENT
    ########################################################################
    def resizeEvent(self, event):
        self.resizeFunction()
        return super(MainWindow, self).resizeEvent(event)

    def resizeFunction(self):
        print('Height: ' + str(self.height()) + ' | Width: ' + str(self.width()))
    ## ==> END ##

    ########################################################################
    ## END ==> APP EVENTS
    ############################## ---/--/--- ##############################

if __name__ == "__main__":
    app = QApplication(sys.argv)
    QtGui.QFontDatabase.addApplicationFont('fonts/segoeui.ttf')
    QtGui.QFontDatabase.addApplicationFont('fonts/segoeuib.ttf')
    QtGui.QFontDatabase.addApplicationFont('fonts/DSEG14ClassicMini-LightItalic.ttf')
    window = MainWindow()
    sys.exit(app.exec_())
