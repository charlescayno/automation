# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'GUI_BASE.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import files_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1900, 1006)
        MainWindow.setMinimumSize(QSize(1000, 720))
        palette = QPalette()
        brush = QBrush(QColor(255, 255, 255, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.WindowText, brush)
        brush1 = QBrush(QColor(0, 0, 0, 0))
        brush1.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Button, brush1)
        brush2 = QBrush(QColor(66, 73, 90, 255))
        brush2.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Light, brush2)
        brush3 = QBrush(QColor(55, 61, 75, 255))
        brush3.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Midlight, brush3)
        brush4 = QBrush(QColor(22, 24, 30, 255))
        brush4.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Dark, brush4)
        brush5 = QBrush(QColor(29, 32, 40, 255))
        brush5.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Mid, brush5)
        brush6 = QBrush(QColor(210, 210, 210, 255))
        brush6.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Text, brush6)
        palette.setBrush(QPalette.Active, QPalette.BrightText, brush)
        palette.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette.setBrush(QPalette.Active, QPalette.Base, brush1)
        palette.setBrush(QPalette.Active, QPalette.Window, brush1)
        brush7 = QBrush(QColor(0, 0, 0, 255))
        brush7.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Shadow, brush7)
        brush8 = QBrush(QColor(85, 170, 255, 255))
        brush8.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Highlight, brush8)
        palette.setBrush(QPalette.Active, QPalette.Link, brush8)
        brush9 = QBrush(QColor(255, 0, 127, 255))
        brush9.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.LinkVisited, brush9)
        palette.setBrush(QPalette.Active, QPalette.AlternateBase, brush4)
        brush10 = QBrush(QColor(44, 49, 60, 255))
        brush10.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.ToolTipBase, brush10)
        palette.setBrush(QPalette.Active, QPalette.ToolTipText, brush6)
        palette.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Button, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Light, brush2)
        palette.setBrush(QPalette.Inactive, QPalette.Midlight, brush3)
        palette.setBrush(QPalette.Inactive, QPalette.Dark, brush4)
        palette.setBrush(QPalette.Inactive, QPalette.Mid, brush5)
        palette.setBrush(QPalette.Inactive, QPalette.Text, brush6)
        palette.setBrush(QPalette.Inactive, QPalette.BrightText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Base, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Window, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Shadow, brush7)
        palette.setBrush(QPalette.Inactive, QPalette.Highlight, brush8)
        palette.setBrush(QPalette.Inactive, QPalette.Link, brush8)
        palette.setBrush(QPalette.Inactive, QPalette.LinkVisited, brush9)
        palette.setBrush(QPalette.Inactive, QPalette.AlternateBase, brush4)
        palette.setBrush(QPalette.Inactive, QPalette.ToolTipBase, brush10)
        palette.setBrush(QPalette.Inactive, QPalette.ToolTipText, brush6)
        palette.setBrush(QPalette.Disabled, QPalette.WindowText, brush4)
        palette.setBrush(QPalette.Disabled, QPalette.Button, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Light, brush2)
        palette.setBrush(QPalette.Disabled, QPalette.Midlight, brush3)
        palette.setBrush(QPalette.Disabled, QPalette.Dark, brush4)
        palette.setBrush(QPalette.Disabled, QPalette.Mid, brush5)
        palette.setBrush(QPalette.Disabled, QPalette.Text, brush4)
        palette.setBrush(QPalette.Disabled, QPalette.BrightText, brush)
        palette.setBrush(QPalette.Disabled, QPalette.ButtonText, brush4)
        palette.setBrush(QPalette.Disabled, QPalette.Base, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Window, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Shadow, brush7)
        brush11 = QBrush(QColor(51, 153, 255, 255))
        brush11.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled, QPalette.Highlight, brush11)
        palette.setBrush(QPalette.Disabled, QPalette.Link, brush8)
        palette.setBrush(QPalette.Disabled, QPalette.LinkVisited, brush9)
        palette.setBrush(QPalette.Disabled, QPalette.AlternateBase, brush10)
        palette.setBrush(QPalette.Disabled, QPalette.ToolTipBase, brush10)
        palette.setBrush(QPalette.Disabled, QPalette.ToolTipText, brush6)
        MainWindow.setPalette(palette)
        font = QFont()
        font.setFamily(u"Segoe UI")
        font.setPointSize(10)
        MainWindow.setFont(font)
        MainWindow.setLayoutDirection(Qt.LeftToRight)
        MainWindow.setStyleSheet(u"QMainWindow {background: transparent; }\n"
"QToolTip {\n"
"	color: #ffffff;\n"
"	background-color: rgba(27, 29, 35, 160);\n"
"	border: 1px solid rgb(40, 40, 40);\n"
"	border-radius: 2px;\n"
"}")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"background: transparent;\n"
"color: rgb(210, 210, 210);")
        self.verticalLayout_13 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_13.setSpacing(0)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.verticalLayout_13.setContentsMargins(10, 10, 10, 10)
        self.frame_main = QFrame(self.centralwidget)
        self.frame_main.setObjectName(u"frame_main")
        self.frame_main.setStyleSheet(u"/* LINE EDIT */\n"
"QLineEdit {\n"
"	background-color: rgb(27, 29, 35);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(27, 29, 35);\n"
"	padding-left: 10px;\n"
"}\n"
"QLineEdit:hover {\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QLineEdit:focus {\n"
"	border: 2px solid rgb(91, 101, 124);\n"
"}\n"
"\n"
"/* SCROLL BARS */\n"
"QScrollBar:horizontal {\n"
"    border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    height: 14px;\n"
"    margin: 0px 21px 0 21px;\n"
"	border-radius: 0px;\n"
"}\n"
"QScrollBar::handle:horizontal {\n"
"    background: rgb(85, 170, 255);\n"
"    min-width: 25px;\n"
"	border-radius: 7px\n"
"}\n"
"QScrollBar::add-line:horizontal {\n"
"    border: none;\n"
"    background: rgb(55, 63, 77);\n"
"    width: 20px;\n"
"	border-top-right-radius: 7px;\n"
"    border-bottom-right-radius: 7px;\n"
"    subcontrol-position: right;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"QScrollBar::sub-line:horizontal {\n"
"    border: none;\n"
"    background: rgb(55, 63, 77);\n"
"    width: 20px;\n"
""
                        "	border-top-left-radius: 7px;\n"
"    border-bottom-left-radius: 7px;\n"
"    subcontrol-position: left;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal\n"
"{\n"
"     background: none;\n"
"}\n"
"QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal\n"
"{\n"
"     background: none;\n"
"}\n"
" QScrollBar:vertical {\n"
"	border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    width: 14px;\n"
"    margin: 21px 0 21px 0;\n"
"	border-radius: 0px;\n"
" }\n"
" QScrollBar::handle:vertical {	\n"
"	background: rgb(85, 170, 255);\n"
"    min-height: 25px;\n"
"	border-radius: 7px\n"
" }\n"
" QScrollBar::add-line:vertical {\n"
"     border: none;\n"
"    background: rgb(55, 63, 77);\n"
"     height: 20px;\n"
"	border-bottom-left-radius: 7px;\n"
"    border-bottom-right-radius: 7px;\n"
"     subcontrol-position: bottom;\n"
"     subcontrol-origin: margin;\n"
" }\n"
" QScrollBar::sub-line:vertical {\n"
"	border: none;\n"
"    background: rgb(55, 63"
                        ", 77);\n"
"     height: 20px;\n"
"	border-top-left-radius: 7px;\n"
"    border-top-right-radius: 7px;\n"
"     subcontrol-position: top;\n"
"     subcontrol-origin: margin;\n"
" }\n"
" QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
"     background: none;\n"
" }\n"
"\n"
" QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
"     background: none;\n"
" }\n"
"\n"
"/* CHECKBOX */\n"
"QCheckBox::indicator {\n"
"    border: 3px solid rgb(52, 59, 72);\n"
"	width: 15px;\n"
"	height: 15px;\n"
"	border-radius: 10px;\n"
"    background: rgb(44, 49, 60);\n"
"}\n"
"QCheckBox::indicator:hover {\n"
"    border: 3px solid rgb(58, 66, 81);\n"
"}\n"
"QCheckBox::indicator:checked {\n"
"    background: 3px solid rgb(52, 59, 72);\n"
"	border: 3px solid rgb(52, 59, 72);	\n"
"	background-image: url(:/16x16/icons/16x16/cil-check-alt.png);\n"
"}\n"
"\n"
"/* RADIO BUTTON */\n"
"QRadioButton::indicator {\n"
"    border: 3px solid rgb(52, 59, 72);\n"
"	width: 15px;\n"
"	height: 15px;\n"
"	border-radius"
                        ": 10px;\n"
"    background: rgb(44, 49, 60);\n"
"}\n"
"QRadioButton::indicator:hover {\n"
"    border: 3px solid rgb(58, 66, 81);\n"
"}\n"
"QRadioButton::indicator:checked {\n"
"    background: 3px solid rgb(94, 106, 130);\n"
"	border: 3px solid rgb(52, 59, 72);	\n"
"}\n"
"\n"
"/* COMBOBOX */\n"
"QComboBox{\n"
"	background-color: rgb(27, 29, 35);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(27, 29, 35);\n"
"	padding: 5px;\n"
"	padding-left: 10px;\n"
"}\n"
"QComboBox:hover{\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QComboBox::drop-down {\n"
"	subcontrol-origin: padding;\n"
"	subcontrol-position: top right;\n"
"	width: 25px; \n"
"	border-left-width: 3px;\n"
"	border-left-color: rgba(39, 44, 54, 150);\n"
"	border-left-style: solid;\n"
"	border-top-right-radius: 3px;\n"
"	border-bottom-right-radius: 3px;	\n"
"	background-image: url(:/16x16/icons/16x16/cil-arrow-bottom.png);\n"
"	background-position: center;\n"
"	background-repeat: no-reperat;\n"
" }\n"
"QComboBox QAbstractItemView {\n"
"	color: rgb("
                        "85, 170, 255);	\n"
"	background-color: rgb(27, 29, 35);\n"
"	padding: 10px;\n"
"	selection-background-color: rgb(39, 44, 54);\n"
"}\n"
"\n"
"/* SLIDERS */\n"
"QSlider::groove:horizontal {\n"
"    border-radius: 9px;\n"
"    height: 18px;\n"
"	margin: 0px;\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"QSlider::groove:horizontal:hover {\n"
"	background-color: rgb(55, 62, 76);\n"
"}\n"
"QSlider::handle:horizontal {\n"
"    background-color: rgb(85, 170, 255);\n"
"    border: none;\n"
"    height: 18px;\n"
"    width: 18px;\n"
"    margin: 0px;\n"
"	border-radius: 9px;\n"
"}\n"
"QSlider::handle:horizontal:hover {\n"
"    background-color: rgb(105, 180, 255);\n"
"}\n"
"QSlider::handle:horizontal:pressed {\n"
"    background-color: rgb(65, 130, 195);\n"
"}\n"
"\n"
"QSlider::groove:vertical {\n"
"    border-radius: 9px;\n"
"    width: 18px;\n"
"    margin: 0px;\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"QSlider::groove:vertical:hover {\n"
"	background-color: rgb(55, 62, 76);\n"
"}\n"
"QSlider::handle:verti"
                        "cal {\n"
"    background-color: rgb(85, 170, 255);\n"
"	border: none;\n"
"    height: 18px;\n"
"    width: 18px;\n"
"    margin: 0px;\n"
"	border-radius: 9px;\n"
"}\n"
"QSlider::handle:vertical:hover {\n"
"    background-color: rgb(105, 180, 255);\n"
"}\n"
"QSlider::handle:vertical:pressed {\n"
"    background-color: rgb(65, 130, 195);\n"
"}\n"
"\n"
"")
        self.frame_main.setFrameShape(QFrame.NoFrame)
        self.frame_main.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.frame_main)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame_top = QFrame(self.frame_main)
        self.frame_top.setObjectName(u"frame_top")
        self.frame_top.setMinimumSize(QSize(0, 65))
        self.frame_top.setMaximumSize(QSize(16777215, 65))
        self.frame_top.setStyleSheet(u"background-color: transparent;")
        self.frame_top.setFrameShape(QFrame.NoFrame)
        self.frame_top.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_top)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.frame_toggle = QFrame(self.frame_top)
        self.frame_toggle.setObjectName(u"frame_toggle")
        self.frame_toggle.setMaximumSize(QSize(70, 16777215))
        self.frame_toggle.setStyleSheet(u"background-color: rgb(27, 29, 35);")
        self.frame_toggle.setFrameShape(QFrame.NoFrame)
        self.frame_toggle.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame_toggle)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.btn_toggle_menu = QPushButton(self.frame_toggle)
        self.btn_toggle_menu.setObjectName(u"btn_toggle_menu")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_toggle_menu.sizePolicy().hasHeightForWidth())
        self.btn_toggle_menu.setSizePolicy(sizePolicy)
        self.btn_toggle_menu.setStyleSheet(u"QPushButton {\n"
"	background-image: url(:/24x24/icons/24x24/cil-menu.png);\n"
"	background-position: center;\n"
"	background-repeat: no-reperat;\n"
"	border: none;\n"
"	background-color: rgb(27, 29, 35);\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(33, 37, 43);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(85, 170, 255);\n"
"}")

        self.verticalLayout_3.addWidget(self.btn_toggle_menu)


        self.horizontalLayout_3.addWidget(self.frame_toggle)

        self.frame_top_right = QFrame(self.frame_top)
        self.frame_top_right.setObjectName(u"frame_top_right")
        self.frame_top_right.setStyleSheet(u"background: transparent;")
        self.frame_top_right.setFrameShape(QFrame.NoFrame)
        self.frame_top_right.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame_top_right)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.frame_top_btns = QFrame(self.frame_top_right)
        self.frame_top_btns.setObjectName(u"frame_top_btns")
        self.frame_top_btns.setMaximumSize(QSize(16777215, 42))
        self.frame_top_btns.setStyleSheet(u"background-color: rgba(27, 29, 35, 200)")
        self.frame_top_btns.setFrameShape(QFrame.NoFrame)
        self.frame_top_btns.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.frame_top_btns)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.frame_label_top_btns = QFrame(self.frame_top_btns)
        self.frame_label_top_btns.setObjectName(u"frame_label_top_btns")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.frame_label_top_btns.sizePolicy().hasHeightForWidth())
        self.frame_label_top_btns.setSizePolicy(sizePolicy1)
        self.frame_label_top_btns.setFrameShape(QFrame.NoFrame)
        self.frame_label_top_btns.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_10 = QHBoxLayout(self.frame_label_top_btns)
        self.horizontalLayout_10.setSpacing(0)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(5, 0, 10, 0)
        self.frame_icon_top_bar = QFrame(self.frame_label_top_btns)
        self.frame_icon_top_bar.setObjectName(u"frame_icon_top_bar")
        self.frame_icon_top_bar.setMaximumSize(QSize(30, 30))
        self.frame_icon_top_bar.setStyleSheet(u"background: transparent;\n"
"background-image: url(:/16x16/icons/16x16/cil-terminal.png);\n"
"background-position: center;\n"
"background-repeat: no-repeat;\n"
"")
        self.frame_icon_top_bar.setFrameShape(QFrame.StyledPanel)
        self.frame_icon_top_bar.setFrameShadow(QFrame.Raised)

        self.horizontalLayout_10.addWidget(self.frame_icon_top_bar)

        self.label_title_bar_top = QLabel(self.frame_label_top_btns)
        self.label_title_bar_top.setObjectName(u"label_title_bar_top")
        font1 = QFont()
        font1.setFamily(u"Segoe UI")
        font1.setPointSize(10)
        font1.setBold(True)
        font1.setWeight(75)
        self.label_title_bar_top.setFont(font1)
        self.label_title_bar_top.setStyleSheet(u"background: transparent;\n"
"")

        self.horizontalLayout_10.addWidget(self.label_title_bar_top)


        self.horizontalLayout_4.addWidget(self.frame_label_top_btns)

        self.frame_btns_right = QFrame(self.frame_top_btns)
        self.frame_btns_right.setObjectName(u"frame_btns_right")
        sizePolicy1.setHeightForWidth(self.frame_btns_right.sizePolicy().hasHeightForWidth())
        self.frame_btns_right.setSizePolicy(sizePolicy1)
        self.frame_btns_right.setMaximumSize(QSize(120, 16777215))
        self.frame_btns_right.setFrameShape(QFrame.NoFrame)
        self.frame_btns_right.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.frame_btns_right)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.btn_minimize = QPushButton(self.frame_btns_right)
        self.btn_minimize.setObjectName(u"btn_minimize")
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.btn_minimize.sizePolicy().hasHeightForWidth())
        self.btn_minimize.setSizePolicy(sizePolicy2)
        self.btn_minimize.setMinimumSize(QSize(40, 0))
        self.btn_minimize.setMaximumSize(QSize(40, 16777215))
        self.btn_minimize.setStyleSheet(u"QPushButton {	\n"
"	border: none;\n"
"	background-color: transparent;\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(85, 170, 255);\n"
"}")
        icon = QIcon()
        icon.addFile(u":/16x16/icons/16x16/cil-window-minimize.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_minimize.setIcon(icon)

        self.horizontalLayout_5.addWidget(self.btn_minimize)

        self.btn_maximize_restore = QPushButton(self.frame_btns_right)
        self.btn_maximize_restore.setObjectName(u"btn_maximize_restore")
        sizePolicy2.setHeightForWidth(self.btn_maximize_restore.sizePolicy().hasHeightForWidth())
        self.btn_maximize_restore.setSizePolicy(sizePolicy2)
        self.btn_maximize_restore.setMinimumSize(QSize(40, 0))
        self.btn_maximize_restore.setMaximumSize(QSize(40, 16777215))
        self.btn_maximize_restore.setStyleSheet(u"QPushButton {	\n"
"	border: none;\n"
"	background-color: transparent;\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(85, 170, 255);\n"
"}")
        icon1 = QIcon()
        icon1.addFile(u":/16x16/icons/16x16/cil-window-maximize.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_maximize_restore.setIcon(icon1)

        self.horizontalLayout_5.addWidget(self.btn_maximize_restore)

        self.btn_close = QPushButton(self.frame_btns_right)
        self.btn_close.setObjectName(u"btn_close")
        sizePolicy2.setHeightForWidth(self.btn_close.sizePolicy().hasHeightForWidth())
        self.btn_close.setSizePolicy(sizePolicy2)
        self.btn_close.setMinimumSize(QSize(40, 0))
        self.btn_close.setMaximumSize(QSize(40, 16777215))
        self.btn_close.setStyleSheet(u"QPushButton {	\n"
"	border: none;\n"
"	background-color: transparent;\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(85, 170, 255);\n"
"}")
        icon2 = QIcon()
        icon2.addFile(u":/16x16/icons/16x16/cil-x.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_close.setIcon(icon2)

        self.horizontalLayout_5.addWidget(self.btn_close)


        self.horizontalLayout_4.addWidget(self.frame_btns_right, 0, Qt.AlignRight)


        self.verticalLayout_2.addWidget(self.frame_top_btns)

        self.frame_top_info = QFrame(self.frame_top_right)
        self.frame_top_info.setObjectName(u"frame_top_info")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(70)
        sizePolicy3.setHeightForWidth(self.frame_top_info.sizePolicy().hasHeightForWidth())
        self.frame_top_info.setSizePolicy(sizePolicy3)
        self.frame_top_info.setMinimumSize(QSize(0, 40))
        self.frame_top_info.setMaximumSize(QSize(16777215, 40))
        font2 = QFont()
        font2.setPointSize(12)
        self.frame_top_info.setFont(font2)
        self.frame_top_info.setStyleSheet(u"background-color: rgb(39, 44, 54);")
        self.frame_top_info.setFrameShape(QFrame.NoFrame)
        self.frame_top_info.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_8 = QHBoxLayout(self.frame_top_info)
        self.horizontalLayout_8.setSpacing(0)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.horizontalLayout_8.setContentsMargins(10, 0, 10, 0)
        self.label_top_info_1 = QLabel(self.frame_top_info)
        self.label_top_info_1.setObjectName(u"label_top_info_1")
        self.label_top_info_1.setMaximumSize(QSize(16777215, 40))
        font3 = QFont()
        font3.setFamily(u"Segoe UI")
        font3.setPointSize(12)
        self.label_top_info_1.setFont(font3)
        self.label_top_info_1.setStyleSheet(u"color: rgb(98, 103, 111); ")
        self.label_top_info_1.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_8.addWidget(self.label_top_info_1)

        self.label_top_info_2 = QLabel(self.frame_top_info)
        self.label_top_info_2.setObjectName(u"label_top_info_2")
        self.label_top_info_2.setMinimumSize(QSize(0, 0))
        self.label_top_info_2.setMaximumSize(QSize(250, 20))
        font4 = QFont()
        font4.setFamily(u"Segoe UI")
        font4.setBold(True)
        font4.setWeight(75)
        self.label_top_info_2.setFont(font4)
        self.label_top_info_2.setStyleSheet(u"color: rgb(98, 103, 111);")
        self.label_top_info_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_8.addWidget(self.label_top_info_2)


        self.verticalLayout_2.addWidget(self.frame_top_info)


        self.horizontalLayout_3.addWidget(self.frame_top_right)


        self.verticalLayout.addWidget(self.frame_top)

        self.frame_center = QFrame(self.frame_main)
        self.frame_center.setObjectName(u"frame_center")
        sizePolicy.setHeightForWidth(self.frame_center.sizePolicy().hasHeightForWidth())
        self.frame_center.setSizePolicy(sizePolicy)
        self.frame_center.setStyleSheet(u"background-color: rgb(40, 44, 52);")
        self.frame_center.setFrameShape(QFrame.NoFrame)
        self.frame_center.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_center)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.frame_left_menu = QFrame(self.frame_center)
        self.frame_left_menu.setObjectName(u"frame_left_menu")
        sizePolicy4 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.frame_left_menu.sizePolicy().hasHeightForWidth())
        self.frame_left_menu.setSizePolicy(sizePolicy4)
        self.frame_left_menu.setMinimumSize(QSize(70, 0))
        self.frame_left_menu.setMaximumSize(QSize(70, 16777215))
        self.frame_left_menu.setLayoutDirection(Qt.LeftToRight)
        self.frame_left_menu.setStyleSheet(u"background-color: rgb(27, 29, 35);")
        self.frame_left_menu.setFrameShape(QFrame.NoFrame)
        self.frame_left_menu.setFrameShadow(QFrame.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.frame_left_menu)
        self.verticalLayout_5.setSpacing(1)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.frame_menus = QFrame(self.frame_left_menu)
        self.frame_menus.setObjectName(u"frame_menus")
        self.frame_menus.setFrameShape(QFrame.NoFrame)
        self.frame_menus.setFrameShadow(QFrame.Raised)
        self.layout_menus = QVBoxLayout(self.frame_menus)
        self.layout_menus.setSpacing(0)
        self.layout_menus.setObjectName(u"layout_menus")
        self.layout_menus.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout_5.addWidget(self.frame_menus, 0, Qt.AlignTop)

        self.frame_extra_menus = QFrame(self.frame_left_menu)
        self.frame_extra_menus.setObjectName(u"frame_extra_menus")
        sizePolicy4.setHeightForWidth(self.frame_extra_menus.sizePolicy().hasHeightForWidth())
        self.frame_extra_menus.setSizePolicy(sizePolicy4)
        self.frame_extra_menus.setFrameShape(QFrame.NoFrame)
        self.frame_extra_menus.setFrameShadow(QFrame.Raised)
        self.layout_menu_bottom = QVBoxLayout(self.frame_extra_menus)
        self.layout_menu_bottom.setSpacing(10)
        self.layout_menu_bottom.setObjectName(u"layout_menu_bottom")
        self.layout_menu_bottom.setContentsMargins(0, 0, 0, 25)
        self.label_user_icon = QLabel(self.frame_extra_menus)
        self.label_user_icon.setObjectName(u"label_user_icon")
        sizePolicy5 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.label_user_icon.sizePolicy().hasHeightForWidth())
        self.label_user_icon.setSizePolicy(sizePolicy5)
        self.label_user_icon.setMinimumSize(QSize(60, 60))
        self.label_user_icon.setMaximumSize(QSize(60, 60))
        self.label_user_icon.setFont(font3)
        self.label_user_icon.setStyleSheet(u"QLabel {\n"
"	border-radius: 30px;\n"
"	background-color: rgb(44, 49, 60);\n"
"	border: 5px solid rgb(39, 44, 54);\n"
"	background-position: center;\n"
"	background-repeat: no-repeat;\n"
"}")
        self.label_user_icon.setAlignment(Qt.AlignCenter)

        self.layout_menu_bottom.addWidget(self.label_user_icon, 0, Qt.AlignHCenter)


        self.verticalLayout_5.addWidget(self.frame_extra_menus, 0, Qt.AlignBottom)


        self.horizontalLayout_2.addWidget(self.frame_left_menu)

        self.frame_content_right = QFrame(self.frame_center)
        self.frame_content_right.setObjectName(u"frame_content_right")
        self.frame_content_right.setStyleSheet(u"background-color: rgb(44, 49, 60);")
        self.frame_content_right.setFrameShape(QFrame.NoFrame)
        self.frame_content_right.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.frame_content_right)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.frame_content = QFrame(self.frame_content_right)
        self.frame_content.setObjectName(u"frame_content")
        self.frame_content.setFrameShape(QFrame.NoFrame)
        self.frame_content.setFrameShadow(QFrame.Raised)
        self.verticalLayout_9 = QVBoxLayout(self.frame_content)
        self.verticalLayout_9.setSpacing(0)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(5, 5, 5, 5)
        self.stackedWidget = QStackedWidget(self.frame_content)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setStyleSheet(u"background: transparent;")
        self.page_home = QWidget()
        self.page_home.setObjectName(u"page_home")
        self.verticalLayout_10 = QVBoxLayout(self.page_home)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.label_6 = QLabel(self.page_home)
        self.label_6.setObjectName(u"label_6")
        font5 = QFont()
        font5.setFamily(u"Segoe UI")
        font5.setPointSize(40)
        self.label_6.setFont(font5)
        self.label_6.setStyleSheet(u"")
        self.label_6.setAlignment(Qt.AlignCenter)

        self.verticalLayout_10.addWidget(self.label_6)

        self.label = QLabel(self.page_home)
        self.label.setObjectName(u"label")
        font6 = QFont()
        font6.setFamily(u"Segoe UI")
        font6.setPointSize(14)
        self.label.setFont(font6)
        self.label.setAlignment(Qt.AlignCenter)

        self.verticalLayout_10.addWidget(self.label)

        self.label_7 = QLabel(self.page_home)
        self.label_7.setObjectName(u"label_7")
        font7 = QFont()
        font7.setFamily(u"Segoe UI")
        font7.setPointSize(15)
        self.label_7.setFont(font7)
        self.label_7.setAlignment(Qt.AlignCenter)

        self.verticalLayout_10.addWidget(self.label_7)

        self.stackedWidget.addWidget(self.page_home)
        self.page_equipment_setup = QWidget()
        self.page_equipment_setup.setObjectName(u"page_equipment_setup")
        self.stackedWidget.addWidget(self.page_equipment_setup)
        self.page_manual_control = QWidget()
        self.page_manual_control.setObjectName(u"page_manual_control")
        self.verticalLayout_12 = QVBoxLayout(self.page_manual_control)
        self.verticalLayout_12.setSpacing(0)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.verticalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.label_manual_control = QFrame(self.page_manual_control)
        self.label_manual_control.setObjectName(u"label_manual_control")
        self.label_manual_control.setMaximumSize(QSize(16777215, 50))
        self.label_manual_control.setStyleSheet(u"background-color: rgb(39, 44, 54);")
        self.label_manual_control.setFrameShape(QFrame.NoFrame)
        self.label_manual_control.setFrameShadow(QFrame.Raised)
        self.verticalLayout_14 = QVBoxLayout(self.label_manual_control)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.label_2 = QLabel(self.label_manual_control)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font1)
        self.label_2.setCursor(QCursor(Qt.UpArrowCursor))

        self.verticalLayout_14.addWidget(self.label_2)


        self.verticalLayout_12.addWidget(self.label_manual_control)

        self.frame_manual_control_upper = QFrame(self.page_manual_control)
        self.frame_manual_control_upper.setObjectName(u"frame_manual_control_upper")
        self.frame_manual_control_upper.setFrameShape(QFrame.NoFrame)
        self.frame_manual_control_upper.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame_manual_control_upper)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame_power_meter_source = QFrame(self.frame_manual_control_upper)
        self.frame_power_meter_source.setObjectName(u"frame_power_meter_source")
        self.frame_power_meter_source.setEnabled(True)
        self.frame_power_meter_source.setStyleSheet(u"QFrame{\n"
"border: 2px solid black;\n"
"border-radius: 10px;\n"
"background-color: rgb(29,34, 44);\n"
"}\n"
"")
        self.frame_power_meter_source.setFrameShape(QFrame.NoFrame)
        self.frame_power_meter_source.setFrameShadow(QFrame.Sunken)
        self.verticalLayout_17 = QVBoxLayout(self.frame_power_meter_source)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.label_source_power_meter = QLabel(self.frame_power_meter_source)
        self.label_source_power_meter.setObjectName(u"label_source_power_meter")
        self.label_source_power_meter.setMaximumSize(QSize(16777215, 30))
        self.label_source_power_meter.setFont(font1)
        self.label_source_power_meter.setCursor(QCursor(Qt.ArrowCursor))
        self.label_source_power_meter.setStyleSheet(u"border:none;")
        self.label_source_power_meter.setAlignment(Qt.AlignCenter)

        self.verticalLayout_17.addWidget(self.label_source_power_meter)

        self.frame_pms_contents = QFrame(self.frame_power_meter_source)
        self.frame_pms_contents.setObjectName(u"frame_pms_contents")
        self.frame_pms_contents.setStyleSheet(u"border:none;")
        self.frame_pms_contents.setFrameShape(QFrame.StyledPanel)
        self.frame_pms_contents.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_14 = QHBoxLayout(self.frame_pms_contents)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.frame_pms_display = QFrame(self.frame_pms_contents)
        self.frame_pms_display.setObjectName(u"frame_pms_display")
        self.frame_pms_display.setMaximumSize(QSize(300, 16777215))
        self.frame_pms_display.setStyleSheet(u"border: 2px solid black;\n"
"border-radius: 10px;\n"
"background-color: rgb(29,34, 44);\n"
"QLabel{\n"
"	font-family: \"Calibri\"\n"
"}")
        self.frame_pms_display.setFrameShape(QFrame.StyledPanel)
        self.frame_pms_display.setFrameShadow(QFrame.Raised)
        self.verticalLayout_16 = QVBoxLayout(self.frame_pms_display)
        self.verticalLayout_16.setSpacing(0)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.verticalLayout_16.setContentsMargins(0, 0, 0, 0)
        self.label_pms_display_a = QLabel(self.frame_pms_display)
        self.label_pms_display_a.setObjectName(u"label_pms_display_a")
        font8 = QFont()
        font8.setFamily(u"Consolas")
        font8.setPointSize(25)
        font8.setBold(False)
        font8.setItalic(False)
        font8.setWeight(50)
        font8.setKerning(False)
        self.label_pms_display_a.setFont(font8)
        self.label_pms_display_a.setStyleSheet(u"color: rgb(255, 0, 0);")
        self.label_pms_display_a.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.verticalLayout_16.addWidget(self.label_pms_display_a)

        self.label_pms_display_b = QLabel(self.frame_pms_display)
        self.label_pms_display_b.setObjectName(u"label_pms_display_b")
        self.label_pms_display_b.setFont(font8)
        self.label_pms_display_b.setStyleSheet(u"color: rgb(255, 0, 0);")
        self.label_pms_display_b.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.verticalLayout_16.addWidget(self.label_pms_display_b)

        self.label_pms_display_c = QLabel(self.frame_pms_display)
        self.label_pms_display_c.setObjectName(u"label_pms_display_c")
        self.label_pms_display_c.setFont(font8)
        self.label_pms_display_c.setStyleSheet(u"color: rgb(255, 0, 0);")
        self.label_pms_display_c.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.verticalLayout_16.addWidget(self.label_pms_display_c)

        self.label_pms_display_d = QLabel(self.frame_pms_display)
        self.label_pms_display_d.setObjectName(u"label_pms_display_d")
        self.label_pms_display_d.setFont(font8)
        self.label_pms_display_d.setStyleSheet(u"color: rgb(255, 0, 0);")
        self.label_pms_display_d.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.verticalLayout_16.addWidget(self.label_pms_display_d)


        self.horizontalLayout_14.addWidget(self.frame_pms_display)

        self.frame_pms_display_select = QFrame(self.frame_pms_contents)
        self.frame_pms_display_select.setObjectName(u"frame_pms_display_select")
        self.frame_pms_display_select.setMaximumSize(QSize(100, 16777215))
        self.frame_pms_display_select.setStyleSheet(u"QFrame{\n"
"border: 2px solid black;\n"
"border-radius: 10px;\n"
"background-color: rgb(29,34, 44);\n"
"}")
        self.frame_pms_display_select.setFrameShape(QFrame.StyledPanel)
        self.frame_pms_display_select.setFrameShadow(QFrame.Raised)
        self.verticalLayout_18 = QVBoxLayout(self.frame_pms_display_select)
        self.verticalLayout_18.setSpacing(0)
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")
        self.verticalLayout_18.setContentsMargins(0, 0, 0, 0)
        self.cbx_pms_display_a = QComboBox(self.frame_pms_display_select)
        self.cbx_pms_display_a.setObjectName(u"cbx_pms_display_a")
        self.cbx_pms_display_a.setMaximumSize(QSize(16777215, 54))

        self.verticalLayout_18.addWidget(self.cbx_pms_display_a)

        self.cbx_pms_display_b = QComboBox(self.frame_pms_display_select)
        self.cbx_pms_display_b.setObjectName(u"cbx_pms_display_b")
        self.cbx_pms_display_b.setMaximumSize(QSize(16777215, 54))

        self.verticalLayout_18.addWidget(self.cbx_pms_display_b)

        self.cbx_pms_display_c = QComboBox(self.frame_pms_display_select)
        self.cbx_pms_display_c.setObjectName(u"cbx_pms_display_c")
        self.cbx_pms_display_c.setMaximumSize(QSize(16777215, 54))

        self.verticalLayout_18.addWidget(self.cbx_pms_display_c)

        self.cbx_pms_display_d = QComboBox(self.frame_pms_display_select)
        self.cbx_pms_display_d.setObjectName(u"cbx_pms_display_d")
        self.cbx_pms_display_d.setMaximumSize(QSize(16777215, 54))

        self.verticalLayout_18.addWidget(self.cbx_pms_display_d)


        self.horizontalLayout_14.addWidget(self.frame_pms_display_select)

        self.frame_pms_control = QFrame(self.frame_pms_contents)
        self.frame_pms_control.setObjectName(u"frame_pms_control")
        self.frame_pms_control.setStyleSheet(u"border: 2px solid black;\n"
"border-radius: 10px;\n"
"background-color: rgb(29,34, 44);\n"
"")
        self.frame_pms_control.setFrameShape(QFrame.StyledPanel)
        self.frame_pms_control.setFrameShadow(QFrame.Raised)
        self.verticalLayout_28 = QVBoxLayout(self.frame_pms_control)
        self.verticalLayout_28.setSpacing(0)
        self.verticalLayout_28.setObjectName(u"verticalLayout_28")
        self.verticalLayout_28.setContentsMargins(0, 0, 0, 0)
        self.frame_pms_control__range = QFrame(self.frame_pms_control)
        self.frame_pms_control__range.setObjectName(u"frame_pms_control__range")
        self.frame_pms_control__range.setFrameShape(QFrame.StyledPanel)
        self.frame_pms_control__range.setFrameShadow(QFrame.Raised)
        self.formLayout = QFormLayout(self.frame_pms_control__range)
        self.formLayout.setObjectName(u"formLayout")
        self.label_pms_voltage_range = QLabel(self.frame_pms_control__range)
        self.label_pms_voltage_range.setObjectName(u"label_pms_voltage_range")
        self.label_pms_voltage_range.setFont(font2)
        self.label_pms_voltage_range.setStyleSheet(u"border:none;")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_pms_voltage_range)

        self.cbx_pms_voltage_range = QComboBox(self.frame_pms_control__range)
        self.cbx_pms_voltage_range.addItem("")
        self.cbx_pms_voltage_range.addItem("")
        self.cbx_pms_voltage_range.setObjectName(u"cbx_pms_voltage_range")
        self.cbx_pms_voltage_range.setMaximumSize(QSize(16777215, 54))
        self.cbx_pms_voltage_range.setFont(font2)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.cbx_pms_voltage_range)

        self.label_pms_current_range = QLabel(self.frame_pms_control__range)
        self.label_pms_current_range.setObjectName(u"label_pms_current_range")
        self.label_pms_current_range.setFont(font2)
        self.label_pms_current_range.setStyleSheet(u"border:none;")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_pms_current_range)

        self.cbx_pms_current_range = QComboBox(self.frame_pms_control__range)
        self.cbx_pms_current_range.addItem("")
        self.cbx_pms_current_range.addItem("")
        self.cbx_pms_current_range.setObjectName(u"cbx_pms_current_range")
        self.cbx_pms_current_range.setMaximumSize(QSize(16777215, 54))
        self.cbx_pms_current_range.setFont(font2)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.cbx_pms_current_range)


        self.verticalLayout_28.addWidget(self.frame_pms_control__range)

        self.frame_pms_control_lower = QFrame(self.frame_pms_control)
        self.frame_pms_control_lower.setObjectName(u"frame_pms_control_lower")
        self.frame_pms_control_lower.setStyleSheet(u"border:none;")
        self.frame_pms_control_lower.setFrameShape(QFrame.StyledPanel)
        self.frame_pms_control_lower.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_18 = QHBoxLayout(self.frame_pms_control_lower)
        self.horizontalLayout_18.setSpacing(0)
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.horizontalLayout_18.setContentsMargins(0, 0, 0, 0)
        self.frame_pms_integration = QFrame(self.frame_pms_control_lower)
        self.frame_pms_integration.setObjectName(u"frame_pms_integration")
        self.frame_pms_integration.setStyleSheet(u"border: 2px solid black;\n"
"border-radius: 10px;")
        self.frame_pms_integration.setFrameShape(QFrame.StyledPanel)
        self.frame_pms_integration.setFrameShadow(QFrame.Raised)
        self.verticalLayout_25 = QVBoxLayout(self.frame_pms_integration)
        self.verticalLayout_25.setObjectName(u"verticalLayout_25")
        self.label_pms_integration = QLabel(self.frame_pms_integration)
        self.label_pms_integration.setObjectName(u"label_pms_integration")
        sizePolicy6 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.label_pms_integration.sizePolicy().hasHeightForWidth())
        self.label_pms_integration.setSizePolicy(sizePolicy6)
        self.label_pms_integration.setMinimumSize(QSize(0, 20))
        self.label_pms_integration.setMaximumSize(QSize(16777215, 20))
        self.label_pms_integration.setFont(font2)
        self.label_pms_integration.setStyleSheet(u"border:none;")

        self.verticalLayout_25.addWidget(self.label_pms_integration)

        self.btn_pms_integration_start = QPushButton(self.frame_pms_integration)
        self.btn_pms_integration_start.setObjectName(u"btn_pms_integration_start")
        self.btn_pms_integration_start.setFont(font2)
        self.btn_pms_integration_start.setStyleSheet(u"QPushButton {\n"
"	border: 2px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(57, 65, 80);\n"
"	border: 2px solid rgb(61, 70, 86);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(35, 40, 49);\n"
"	border: 2px solid rgb(43, 50, 61);\n"
"}")

        self.verticalLayout_25.addWidget(self.btn_pms_integration_start)

        self.btn_pms_integration_stop = QPushButton(self.frame_pms_integration)
        self.btn_pms_integration_stop.setObjectName(u"btn_pms_integration_stop")
        self.btn_pms_integration_stop.setFont(font2)
        self.btn_pms_integration_stop.setStyleSheet(u"QPushButton {\n"
"	border: 2px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(57, 65, 80);\n"
"	border: 2px solid rgb(61, 70, 86);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(35, 40, 49);\n"
"	border: 2px solid rgb(43, 50, 61);\n"
"}")

        self.verticalLayout_25.addWidget(self.btn_pms_integration_stop)

        self.btn_pms_integration_reset = QPushButton(self.frame_pms_integration)
        self.btn_pms_integration_reset.setObjectName(u"btn_pms_integration_reset")
        self.btn_pms_integration_reset.setFont(font2)
        self.btn_pms_integration_reset.setStyleSheet(u"QPushButton {\n"
"	border: 2px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(57, 65, 80);\n"
"	border: 2px solid rgb(61, 70, 86);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(35, 40, 49);\n"
"	border: 2px solid rgb(43, 50, 61);\n"
"}")

        self.verticalLayout_25.addWidget(self.btn_pms_integration_reset)


        self.horizontalLayout_18.addWidget(self.frame_pms_integration)

        self.frame_pms_averaging = QFrame(self.frame_pms_control_lower)
        self.frame_pms_averaging.setObjectName(u"frame_pms_averaging")
        self.frame_pms_averaging.setStyleSheet(u"border: 2px solid black;\n"
"border-radius: 10px;")
        self.frame_pms_averaging.setFrameShape(QFrame.StyledPanel)
        self.frame_pms_averaging.setFrameShadow(QFrame.Raised)
        self.verticalLayout_26 = QVBoxLayout(self.frame_pms_averaging)
        self.verticalLayout_26.setSpacing(2)
        self.verticalLayout_26.setObjectName(u"verticalLayout_26")
        self.verticalLayout_26.setContentsMargins(-1, 5, -1, 5)
        self.label_pms_averaging = QLabel(self.frame_pms_averaging)
        self.label_pms_averaging.setObjectName(u"label_pms_averaging")
        sizePolicy6.setHeightForWidth(self.label_pms_averaging.sizePolicy().hasHeightForWidth())
        self.label_pms_averaging.setSizePolicy(sizePolicy6)
        self.label_pms_averaging.setMinimumSize(QSize(0, 20))
        self.label_pms_averaging.setMaximumSize(QSize(16777215, 20))
        self.label_pms_averaging.setFont(font2)
        self.label_pms_averaging.setStyleSheet(u"border:none;")

        self.verticalLayout_26.addWidget(self.label_pms_averaging)

        self.btn_pms_averaging_toggle = QPushButton(self.frame_pms_averaging)
        self.btn_pms_averaging_toggle.setObjectName(u"btn_pms_averaging_toggle")
        self.btn_pms_averaging_toggle.setFont(font2)
        self.btn_pms_averaging_toggle.setStyleSheet(u"QPushButton {\n"
"	border: 2px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(57, 65, 80);\n"
"	border: 2px solid rgb(61, 70, 86);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(35, 40, 49);\n"
"	border: 2px solid rgb(43, 50, 61);\n"
"}")

        self.verticalLayout_26.addWidget(self.btn_pms_averaging_toggle)

        self.cbx_pms_averaging_count = QComboBox(self.frame_pms_averaging)
        self.cbx_pms_averaging_count.addItem("")
        self.cbx_pms_averaging_count.addItem("")
        self.cbx_pms_averaging_count.addItem("")
        self.cbx_pms_averaging_count.setObjectName(u"cbx_pms_averaging_count")
        self.cbx_pms_averaging_count.setMaximumSize(QSize(16777215, 40))
        self.cbx_pms_averaging_count.setFont(font2)

        self.verticalLayout_26.addWidget(self.cbx_pms_averaging_count)

        self.cbx_pms_averaging_mode = QComboBox(self.frame_pms_averaging)
        self.cbx_pms_averaging_mode.addItem("")
        self.cbx_pms_averaging_mode.addItem("")
        self.cbx_pms_averaging_mode.setObjectName(u"cbx_pms_averaging_mode")
        self.cbx_pms_averaging_mode.setMaximumSize(QSize(16777215, 40))
        self.cbx_pms_averaging_mode.setFont(font2)

        self.verticalLayout_26.addWidget(self.cbx_pms_averaging_mode)


        self.horizontalLayout_18.addWidget(self.frame_pms_averaging)

        self.frame_pms_measure_mode = QFrame(self.frame_pms_control_lower)
        self.frame_pms_measure_mode.setObjectName(u"frame_pms_measure_mode")
        self.frame_pms_measure_mode.setStyleSheet(u"border: 2px solid black;\n"
"border-radius: 10px;")
        self.frame_pms_measure_mode.setFrameShape(QFrame.StyledPanel)
        self.frame_pms_measure_mode.setFrameShadow(QFrame.Raised)
        self.verticalLayout_27 = QVBoxLayout(self.frame_pms_measure_mode)
        self.verticalLayout_27.setSpacing(13)
        self.verticalLayout_27.setObjectName(u"verticalLayout_27")
        self.verticalLayout_27.setContentsMargins(13, 13, 13, 13)
        self.label_pms_measure_mode = QLabel(self.frame_pms_measure_mode)
        self.label_pms_measure_mode.setObjectName(u"label_pms_measure_mode")
        sizePolicy6.setHeightForWidth(self.label_pms_measure_mode.sizePolicy().hasHeightForWidth())
        self.label_pms_measure_mode.setSizePolicy(sizePolicy6)
        self.label_pms_measure_mode.setMaximumSize(QSize(16777215, 20))
        self.label_pms_measure_mode.setFont(font2)
        self.label_pms_measure_mode.setStyleSheet(u"border:none;")

        self.verticalLayout_27.addWidget(self.label_pms_measure_mode)

        self.btn_pms_measure_mode = QPushButton(self.frame_pms_measure_mode)
        self.btn_pms_measure_mode.setObjectName(u"btn_pms_measure_mode")
        self.btn_pms_measure_mode.setFont(font2)
        self.btn_pms_measure_mode.setStyleSheet(u"QPushButton {\n"
"	border: 2px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(57, 65, 80);\n"
"	border: 2px solid rgb(61, 70, 86);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(35, 40, 49);\n"
"	border: 2px solid rgb(43, 50, 61);\n"
"}")

        self.verticalLayout_27.addWidget(self.btn_pms_measure_mode)


        self.horizontalLayout_18.addWidget(self.frame_pms_measure_mode)


        self.verticalLayout_28.addWidget(self.frame_pms_control_lower)


        self.horizontalLayout_14.addWidget(self.frame_pms_control)


        self.verticalLayout_17.addWidget(self.frame_pms_contents)


        self.horizontalLayout.addWidget(self.frame_power_meter_source)

        self.frame_power_meter_load = QFrame(self.frame_manual_control_upper)
        self.frame_power_meter_load.setObjectName(u"frame_power_meter_load")
        self.frame_power_meter_load.setEnabled(True)
        self.frame_power_meter_load.setMinimumSize(QSize(0, 420))
        self.frame_power_meter_load.setStyleSheet(u"QFrame{\n"
"border: 2px solid black;\n"
"border-radius: 10px;\n"
"background-color: rgb(29,34, 44);\n"
"}\n"
"")
        self.frame_power_meter_load.setFrameShape(QFrame.NoFrame)
        self.frame_power_meter_load.setFrameShadow(QFrame.Sunken)
        self.verticalLayout_19 = QVBoxLayout(self.frame_power_meter_load)
        self.verticalLayout_19.setObjectName(u"verticalLayout_19")
        self.label_source_power_meter_2 = QLabel(self.frame_power_meter_load)
        self.label_source_power_meter_2.setObjectName(u"label_source_power_meter_2")
        self.label_source_power_meter_2.setMaximumSize(QSize(16777215, 30))
        self.label_source_power_meter_2.setFont(font1)
        self.label_source_power_meter_2.setCursor(QCursor(Qt.ArrowCursor))
        self.label_source_power_meter_2.setStyleSheet(u"border:none;")
        self.label_source_power_meter_2.setAlignment(Qt.AlignCenter)

        self.verticalLayout_19.addWidget(self.label_source_power_meter_2)

        self.frame_pml_contents = QFrame(self.frame_power_meter_load)
        self.frame_pml_contents.setObjectName(u"frame_pml_contents")
        self.frame_pml_contents.setStyleSheet(u"border:none;")
        self.frame_pml_contents.setFrameShape(QFrame.StyledPanel)
        self.frame_pml_contents.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_15 = QHBoxLayout(self.frame_pml_contents)
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.frame_pml_display = QFrame(self.frame_pml_contents)
        self.frame_pml_display.setObjectName(u"frame_pml_display")
        self.frame_pml_display.setMaximumSize(QSize(300, 16777215))
        self.frame_pml_display.setStyleSheet(u"border: 2px solid black;\n"
"border-radius: 10px;\n"
"background-color: rgb(29,34, 44);\n"
"QLabel{\n"
"	font-family: \"Calibri\"\n"
"}")
        self.frame_pml_display.setFrameShape(QFrame.StyledPanel)
        self.frame_pml_display.setFrameShadow(QFrame.Raised)
        self.verticalLayout_20 = QVBoxLayout(self.frame_pml_display)
        self.verticalLayout_20.setSpacing(0)
        self.verticalLayout_20.setObjectName(u"verticalLayout_20")
        self.verticalLayout_20.setContentsMargins(0, 0, 0, 0)
        self.label_pml_display_a = QLabel(self.frame_pml_display)
        self.label_pml_display_a.setObjectName(u"label_pml_display_a")
        self.label_pml_display_a.setFont(font8)
        self.label_pml_display_a.setStyleSheet(u"color: rgb(255, 0, 0);")
        self.label_pml_display_a.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.verticalLayout_20.addWidget(self.label_pml_display_a)

        self.label_pml_display_b = QLabel(self.frame_pml_display)
        self.label_pml_display_b.setObjectName(u"label_pml_display_b")
        self.label_pml_display_b.setFont(font8)
        self.label_pml_display_b.setStyleSheet(u"color: rgb(255, 0, 0);")
        self.label_pml_display_b.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.verticalLayout_20.addWidget(self.label_pml_display_b)

        self.label_pml_display_c = QLabel(self.frame_pml_display)
        self.label_pml_display_c.setObjectName(u"label_pml_display_c")
        font9 = QFont()
        font9.setFamily(u"Consolas")
        font9.setPointSize(24)
        font9.setBold(False)
        font9.setItalic(False)
        font9.setWeight(50)
        font9.setKerning(False)
        self.label_pml_display_c.setFont(font9)
        self.label_pml_display_c.setStyleSheet(u"color: rgb(255, 0, 0);")
        self.label_pml_display_c.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.verticalLayout_20.addWidget(self.label_pml_display_c)

        self.label_pml_display_d = QLabel(self.frame_pml_display)
        self.label_pml_display_d.setObjectName(u"label_pml_display_d")
        self.label_pml_display_d.setFont(font8)
        self.label_pml_display_d.setStyleSheet(u"color: rgb(255, 0, 0);")
        self.label_pml_display_d.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.verticalLayout_20.addWidget(self.label_pml_display_d)


        self.horizontalLayout_15.addWidget(self.frame_pml_display)

        self.frame_pml_display_select = QFrame(self.frame_pml_contents)
        self.frame_pml_display_select.setObjectName(u"frame_pml_display_select")
        self.frame_pml_display_select.setMaximumSize(QSize(100, 16777215))
        self.frame_pml_display_select.setStyleSheet(u"QFrame{\n"
"border: 2px solid black;\n"
"border-radius: 10px;\n"
"background-color: rgb(29,34, 44);\n"
"}")
        self.frame_pml_display_select.setFrameShape(QFrame.StyledPanel)
        self.frame_pml_display_select.setFrameShadow(QFrame.Raised)
        self.verticalLayout_21 = QVBoxLayout(self.frame_pml_display_select)
        self.verticalLayout_21.setSpacing(0)
        self.verticalLayout_21.setObjectName(u"verticalLayout_21")
        self.verticalLayout_21.setContentsMargins(0, 0, 0, 0)
        self.cbx_pml_display_a = QComboBox(self.frame_pml_display_select)
        self.cbx_pml_display_a.setObjectName(u"cbx_pml_display_a")
        self.cbx_pml_display_a.setMaximumSize(QSize(16777215, 54))

        self.verticalLayout_21.addWidget(self.cbx_pml_display_a)

        self.cbx_pml_display_b = QComboBox(self.frame_pml_display_select)
        self.cbx_pml_display_b.setObjectName(u"cbx_pml_display_b")
        self.cbx_pml_display_b.setMaximumSize(QSize(16777215, 54))

        self.verticalLayout_21.addWidget(self.cbx_pml_display_b)

        self.cbx_pml_display_c = QComboBox(self.frame_pml_display_select)
        self.cbx_pml_display_c.setObjectName(u"cbx_pml_display_c")
        self.cbx_pml_display_c.setMaximumSize(QSize(16777215, 54))

        self.verticalLayout_21.addWidget(self.cbx_pml_display_c)

        self.cbx_pml_display_d = QComboBox(self.frame_pml_display_select)
        self.cbx_pml_display_d.setObjectName(u"cbx_pml_display_d")
        self.cbx_pml_display_d.setMaximumSize(QSize(16777215, 54))

        self.verticalLayout_21.addWidget(self.cbx_pml_display_d)


        self.horizontalLayout_15.addWidget(self.frame_pml_display_select)

        self.frame_pml_control = QFrame(self.frame_pml_contents)
        self.frame_pml_control.setObjectName(u"frame_pml_control")
        self.frame_pml_control.setStyleSheet(u"border: 2px solid black;\n"
"border-radius: 10px;\n"
"background-color: rgb(29,34, 44);\n"
"")
        self.frame_pml_control.setFrameShape(QFrame.StyledPanel)
        self.frame_pml_control.setFrameShadow(QFrame.Raised)
        self.verticalLayout_29 = QVBoxLayout(self.frame_pml_control)
        self.verticalLayout_29.setSpacing(0)
        self.verticalLayout_29.setObjectName(u"verticalLayout_29")
        self.verticalLayout_29.setContentsMargins(0, 0, 0, 0)
        self.frame_pml_control__range = QFrame(self.frame_pml_control)
        self.frame_pml_control__range.setObjectName(u"frame_pml_control__range")
        self.frame_pml_control__range.setFrameShape(QFrame.StyledPanel)
        self.frame_pml_control__range.setFrameShadow(QFrame.Raised)
        self.formLayout_2 = QFormLayout(self.frame_pml_control__range)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.label_pms_voltage_range_2 = QLabel(self.frame_pml_control__range)
        self.label_pms_voltage_range_2.setObjectName(u"label_pms_voltage_range_2")
        self.label_pms_voltage_range_2.setFont(font2)
        self.label_pms_voltage_range_2.setStyleSheet(u"border:none;")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.label_pms_voltage_range_2)

        self.cbx_pms_voltage_range_2 = QComboBox(self.frame_pml_control__range)
        self.cbx_pms_voltage_range_2.addItem("")
        self.cbx_pms_voltage_range_2.addItem("")
        self.cbx_pms_voltage_range_2.setObjectName(u"cbx_pms_voltage_range_2")
        self.cbx_pms_voltage_range_2.setMaximumSize(QSize(16777215, 54))
        self.cbx_pms_voltage_range_2.setFont(font2)

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.cbx_pms_voltage_range_2)

        self.label_pms_current_range_2 = QLabel(self.frame_pml_control__range)
        self.label_pms_current_range_2.setObjectName(u"label_pms_current_range_2")
        self.label_pms_current_range_2.setFont(font2)
        self.label_pms_current_range_2.setStyleSheet(u"border:none;")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.label_pms_current_range_2)

        self.cbx_pms_current_range_2 = QComboBox(self.frame_pml_control__range)
        self.cbx_pms_current_range_2.addItem("")
        self.cbx_pms_current_range_2.addItem("")
        self.cbx_pms_current_range_2.setObjectName(u"cbx_pms_current_range_2")
        self.cbx_pms_current_range_2.setMaximumSize(QSize(16777215, 54))
        self.cbx_pms_current_range_2.setFont(font2)

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.cbx_pms_current_range_2)


        self.verticalLayout_29.addWidget(self.frame_pml_control__range)

        self.frame_pms_control_lower_2 = QFrame(self.frame_pml_control)
        self.frame_pms_control_lower_2.setObjectName(u"frame_pms_control_lower_2")
        self.frame_pms_control_lower_2.setStyleSheet(u"border:none;")
        self.frame_pms_control_lower_2.setFrameShape(QFrame.StyledPanel)
        self.frame_pms_control_lower_2.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_19 = QHBoxLayout(self.frame_pms_control_lower_2)
        self.horizontalLayout_19.setSpacing(0)
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.horizontalLayout_19.setContentsMargins(0, 0, 0, 0)
        self.frame_pml_integration = QFrame(self.frame_pms_control_lower_2)
        self.frame_pml_integration.setObjectName(u"frame_pml_integration")
        self.frame_pml_integration.setStyleSheet(u"border: 2px solid black;\n"
"border-radius: 10px;")
        self.frame_pml_integration.setFrameShape(QFrame.StyledPanel)
        self.frame_pml_integration.setFrameShadow(QFrame.Raised)
        self.verticalLayout_30 = QVBoxLayout(self.frame_pml_integration)
        self.verticalLayout_30.setObjectName(u"verticalLayout_30")
        self.label_pms_integration_2 = QLabel(self.frame_pml_integration)
        self.label_pms_integration_2.setObjectName(u"label_pms_integration_2")
        sizePolicy6.setHeightForWidth(self.label_pms_integration_2.sizePolicy().hasHeightForWidth())
        self.label_pms_integration_2.setSizePolicy(sizePolicy6)
        self.label_pms_integration_2.setMinimumSize(QSize(0, 20))
        self.label_pms_integration_2.setMaximumSize(QSize(16777215, 20))
        font10 = QFont()
        font10.setFamily(u"Segoe UI Emoji")
        font10.setPointSize(12)
        self.label_pms_integration_2.setFont(font10)
        self.label_pms_integration_2.setStyleSheet(u"border:none;")
        self.label_pms_integration_2.setAlignment(Qt.AlignCenter)

        self.verticalLayout_30.addWidget(self.label_pms_integration_2)

        self.btn_pms_integration_start_2 = QPushButton(self.frame_pml_integration)
        self.btn_pms_integration_start_2.setObjectName(u"btn_pms_integration_start_2")
        self.btn_pms_integration_start_2.setFont(font2)
        self.btn_pms_integration_start_2.setStyleSheet(u"QPushButton {\n"
"	border: 2px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(57, 65, 80);\n"
"	border: 2px solid rgb(61, 70, 86);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(35, 40, 49);\n"
"	border: 2px solid rgb(43, 50, 61);\n"
"}")

        self.verticalLayout_30.addWidget(self.btn_pms_integration_start_2)

        self.btn_pms_integration_stop_2 = QPushButton(self.frame_pml_integration)
        self.btn_pms_integration_stop_2.setObjectName(u"btn_pms_integration_stop_2")
        self.btn_pms_integration_stop_2.setFont(font2)
        self.btn_pms_integration_stop_2.setStyleSheet(u"QPushButton {\n"
"	border: 2px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(57, 65, 80);\n"
"	border: 2px solid rgb(61, 70, 86);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(35, 40, 49);\n"
"	border: 2px solid rgb(43, 50, 61);\n"
"}")

        self.verticalLayout_30.addWidget(self.btn_pms_integration_stop_2)

        self.btn_pms_integration_reset_2 = QPushButton(self.frame_pml_integration)
        self.btn_pms_integration_reset_2.setObjectName(u"btn_pms_integration_reset_2")
        self.btn_pms_integration_reset_2.setFont(font2)
        self.btn_pms_integration_reset_2.setStyleSheet(u"QPushButton {\n"
"	border: 2px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(57, 65, 80);\n"
"	border: 2px solid rgb(61, 70, 86);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(35, 40, 49);\n"
"	border: 2px solid rgb(43, 50, 61);\n"
"}")

        self.verticalLayout_30.addWidget(self.btn_pms_integration_reset_2)


        self.horizontalLayout_19.addWidget(self.frame_pml_integration)

        self.frame_pms_averaging_2 = QFrame(self.frame_pms_control_lower_2)
        self.frame_pms_averaging_2.setObjectName(u"frame_pms_averaging_2")
        self.frame_pms_averaging_2.setStyleSheet(u"border: 2px solid black;\n"
"border-radius: 10px;")
        self.frame_pms_averaging_2.setFrameShape(QFrame.StyledPanel)
        self.frame_pms_averaging_2.setFrameShadow(QFrame.Raised)
        self.verticalLayout_31 = QVBoxLayout(self.frame_pms_averaging_2)
        self.verticalLayout_31.setSpacing(2)
        self.verticalLayout_31.setObjectName(u"verticalLayout_31")
        self.verticalLayout_31.setContentsMargins(-1, 5, -1, 5)
        self.label_pms_averaging_2 = QLabel(self.frame_pms_averaging_2)
        self.label_pms_averaging_2.setObjectName(u"label_pms_averaging_2")
        sizePolicy6.setHeightForWidth(self.label_pms_averaging_2.sizePolicy().hasHeightForWidth())
        self.label_pms_averaging_2.setSizePolicy(sizePolicy6)
        self.label_pms_averaging_2.setMinimumSize(QSize(0, 20))
        self.label_pms_averaging_2.setMaximumSize(QSize(16777215, 20))
        self.label_pms_averaging_2.setFont(font2)
        self.label_pms_averaging_2.setStyleSheet(u"border:none;")
        self.label_pms_averaging_2.setAlignment(Qt.AlignCenter)

        self.verticalLayout_31.addWidget(self.label_pms_averaging_2)

        self.btn_pms_averaging_toggle_2 = QPushButton(self.frame_pms_averaging_2)
        self.btn_pms_averaging_toggle_2.setObjectName(u"btn_pms_averaging_toggle_2")
        self.btn_pms_averaging_toggle_2.setFont(font2)
        self.btn_pms_averaging_toggle_2.setStyleSheet(u"QPushButton {\n"
"	border: 2px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(57, 65, 80);\n"
"	border: 2px solid rgb(61, 70, 86);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(35, 40, 49);\n"
"	border: 2px solid rgb(43, 50, 61);\n"
"}")

        self.verticalLayout_31.addWidget(self.btn_pms_averaging_toggle_2)

        self.cbx_pms_averaging_count_2 = QComboBox(self.frame_pms_averaging_2)
        self.cbx_pms_averaging_count_2.addItem("")
        self.cbx_pms_averaging_count_2.addItem("")
        self.cbx_pms_averaging_count_2.addItem("")
        self.cbx_pms_averaging_count_2.setObjectName(u"cbx_pms_averaging_count_2")
        self.cbx_pms_averaging_count_2.setMaximumSize(QSize(16777215, 40))
        self.cbx_pms_averaging_count_2.setFont(font2)

        self.verticalLayout_31.addWidget(self.cbx_pms_averaging_count_2)

        self.cbx_pml_averaging_mode = QComboBox(self.frame_pms_averaging_2)
        self.cbx_pml_averaging_mode.addItem("")
        self.cbx_pml_averaging_mode.addItem("")
        self.cbx_pml_averaging_mode.setObjectName(u"cbx_pml_averaging_mode")
        self.cbx_pml_averaging_mode.setMaximumSize(QSize(16777215, 40))
        self.cbx_pml_averaging_mode.setFont(font2)

        self.verticalLayout_31.addWidget(self.cbx_pml_averaging_mode)


        self.horizontalLayout_19.addWidget(self.frame_pms_averaging_2)

        self.frame_pms_measure_mode_2 = QFrame(self.frame_pms_control_lower_2)
        self.frame_pms_measure_mode_2.setObjectName(u"frame_pms_measure_mode_2")
        self.frame_pms_measure_mode_2.setStyleSheet(u"border: 2px solid black;\n"
"border-radius: 10px;")
        self.frame_pms_measure_mode_2.setFrameShape(QFrame.StyledPanel)
        self.frame_pms_measure_mode_2.setFrameShadow(QFrame.Raised)
        self.verticalLayout_32 = QVBoxLayout(self.frame_pms_measure_mode_2)
        self.verticalLayout_32.setSpacing(13)
        self.verticalLayout_32.setObjectName(u"verticalLayout_32")
        self.verticalLayout_32.setContentsMargins(13, 13, 13, 13)
        self.label_pms_measure_mode_2 = QLabel(self.frame_pms_measure_mode_2)
        self.label_pms_measure_mode_2.setObjectName(u"label_pms_measure_mode_2")
        sizePolicy6.setHeightForWidth(self.label_pms_measure_mode_2.sizePolicy().hasHeightForWidth())
        self.label_pms_measure_mode_2.setSizePolicy(sizePolicy6)
        self.label_pms_measure_mode_2.setMaximumSize(QSize(16777215, 20))
        self.label_pms_measure_mode_2.setFont(font2)
        self.label_pms_measure_mode_2.setStyleSheet(u"border:none;")
        self.label_pms_measure_mode_2.setAlignment(Qt.AlignCenter)

        self.verticalLayout_32.addWidget(self.label_pms_measure_mode_2)

        self.btn_pms_measure_mode_2 = QPushButton(self.frame_pms_measure_mode_2)
        self.btn_pms_measure_mode_2.setObjectName(u"btn_pms_measure_mode_2")
        self.btn_pms_measure_mode_2.setFont(font2)
        self.btn_pms_measure_mode_2.setStyleSheet(u"QPushButton {\n"
"	border: 2px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(57, 65, 80);\n"
"	border: 2px solid rgb(61, 70, 86);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(35, 40, 49);\n"
"	border: 2px solid rgb(43, 50, 61);\n"
"}")

        self.verticalLayout_32.addWidget(self.btn_pms_measure_mode_2)


        self.horizontalLayout_19.addWidget(self.frame_pms_measure_mode_2)


        self.verticalLayout_29.addWidget(self.frame_pms_control_lower_2)


        self.horizontalLayout_15.addWidget(self.frame_pml_control)


        self.verticalLayout_19.addWidget(self.frame_pml_contents)


        self.horizontalLayout.addWidget(self.frame_power_meter_load)


        self.verticalLayout_12.addWidget(self.frame_manual_control_upper)

        self.frame_manual_control_lower = QFrame(self.page_manual_control)
        self.frame_manual_control_lower.setObjectName(u"frame_manual_control_lower")
        self.frame_manual_control_lower.setStyleSheet(u"")
        self.frame_manual_control_lower.setFrameShape(QFrame.NoFrame)
        self.frame_manual_control_lower.setFrameShadow(QFrame.Raised)
        self.frame_manual_control_lower.setLineWidth(0)
        self.horizontalLayout_13 = QHBoxLayout(self.frame_manual_control_lower)
        self.horizontalLayout_13.setSpacing(0)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.frame_ac_source = QFrame(self.frame_manual_control_lower)
        self.frame_ac_source.setObjectName(u"frame_ac_source")
        self.frame_ac_source.setMinimumSize(QSize(600, 0))
        self.frame_ac_source.setStyleSheet(u"QFrame{\n"
"border: 2px solid black;\n"
"border-radius: 10px;\n"
"background-color: rgb(29,34, 44);\n"
"}")
        self.frame_ac_source.setFrameShape(QFrame.StyledPanel)
        self.frame_ac_source.setFrameShadow(QFrame.Raised)
        self.verticalLayout_24 = QVBoxLayout(self.frame_ac_source)
        self.verticalLayout_24.setObjectName(u"verticalLayout_24")
        self.label_source_ac_source = QLabel(self.frame_ac_source)
        self.label_source_ac_source.setObjectName(u"label_source_ac_source")
        self.label_source_ac_source.setMaximumSize(QSize(16777215, 30))
        self.label_source_ac_source.setFont(font1)
        self.label_source_ac_source.setCursor(QCursor(Qt.UpArrowCursor))
        self.label_source_ac_source.setStyleSheet(u"border:none;")
        self.label_source_ac_source.setAlignment(Qt.AlignCenter)

        self.verticalLayout_24.addWidget(self.label_source_ac_source)

        self.frame_ac_source_contents = QFrame(self.frame_ac_source)
        self.frame_ac_source_contents.setObjectName(u"frame_ac_source_contents")
        self.frame_ac_source_contents.setStyleSheet(u"border:none;")
        self.frame_ac_source_contents.setFrameShape(QFrame.StyledPanel)
        self.frame_ac_source_contents.setFrameShadow(QFrame.Raised)

        self.verticalLayout_24.addWidget(self.frame_ac_source_contents)


        self.horizontalLayout_13.addWidget(self.frame_ac_source)

        self.frame_electronic_load = QFrame(self.frame_manual_control_lower)
        self.frame_electronic_load.setObjectName(u"frame_electronic_load")
        self.frame_electronic_load.setMinimumSize(QSize(600, 0))
        self.frame_electronic_load.setStyleSheet(u"QFrame{\n"
"border: 2px solid black;\n"
"border-radius: 10px;\n"
"background-color: rgb(29,34, 44);\n"
"}")
        self.frame_electronic_load.setFrameShape(QFrame.StyledPanel)
        self.frame_electronic_load.setFrameShadow(QFrame.Raised)
        self.verticalLayout_23 = QVBoxLayout(self.frame_electronic_load)
        self.verticalLayout_23.setObjectName(u"verticalLayout_23")
        self.label_eload = QLabel(self.frame_electronic_load)
        self.label_eload.setObjectName(u"label_eload")
        self.label_eload.setMaximumSize(QSize(16777215, 30))
        self.label_eload.setFont(font1)
        self.label_eload.setCursor(QCursor(Qt.UpArrowCursor))
        self.label_eload.setStyleSheet(u"border:none;")
        self.label_eload.setAlignment(Qt.AlignCenter)

        self.verticalLayout_23.addWidget(self.label_eload)

        self.frame_eload_contents = QFrame(self.frame_electronic_load)
        self.frame_eload_contents.setObjectName(u"frame_eload_contents")
        self.frame_eload_contents.setStyleSheet(u"border:none;")
        self.frame_eload_contents.setFrameShape(QFrame.StyledPanel)
        self.frame_eload_contents.setFrameShadow(QFrame.Raised)

        self.verticalLayout_23.addWidget(self.frame_eload_contents)


        self.horizontalLayout_13.addWidget(self.frame_electronic_load)

        self.frame_usb_pd_sink = QFrame(self.frame_manual_control_lower)
        self.frame_usb_pd_sink.setObjectName(u"frame_usb_pd_sink")
        self.frame_usb_pd_sink.setMinimumSize(QSize(600, 0))
        self.frame_usb_pd_sink.setStyleSheet(u"QFrame{\n"
"	border: 2px solid black;\n"
"	border-radius: 10px;\n"
"	background-color: rgb(29,34, 44);\n"
"}")
        self.frame_usb_pd_sink.setFrameShape(QFrame.StyledPanel)
        self.frame_usb_pd_sink.setFrameShadow(QFrame.Raised)
        self.verticalLayout_22 = QVBoxLayout(self.frame_usb_pd_sink)
        self.verticalLayout_22.setObjectName(u"verticalLayout_22")
        self.label_source_power_meter_5 = QLabel(self.frame_usb_pd_sink)
        self.label_source_power_meter_5.setObjectName(u"label_source_power_meter_5")
        self.label_source_power_meter_5.setMaximumSize(QSize(16777215, 30))
        self.label_source_power_meter_5.setFont(font1)
        self.label_source_power_meter_5.setCursor(QCursor(Qt.UpArrowCursor))
        self.label_source_power_meter_5.setStyleSheet(u"border:none;")
        self.label_source_power_meter_5.setAlignment(Qt.AlignCenter)

        self.verticalLayout_22.addWidget(self.label_source_power_meter_5)

        self.frame_usb_pd_sink_contents = QFrame(self.frame_usb_pd_sink)
        self.frame_usb_pd_sink_contents.setObjectName(u"frame_usb_pd_sink_contents")
        self.frame_usb_pd_sink_contents.setStyleSheet(u"border:none;")
        self.frame_usb_pd_sink_contents.setFrameShape(QFrame.StyledPanel)
        self.frame_usb_pd_sink_contents.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_16 = QHBoxLayout(self.frame_usb_pd_sink_contents)
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.frame_5 = QFrame(self.frame_usb_pd_sink_contents)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.verticalLayout_33 = QVBoxLayout(self.frame_5)
        self.verticalLayout_33.setObjectName(u"verticalLayout_33")
        self.label_usbpdsink_sourcecaps = QLabel(self.frame_5)
        self.label_usbpdsink_sourcecaps.setObjectName(u"label_usbpdsink_sourcecaps")
        self.label_usbpdsink_sourcecaps.setMaximumSize(QSize(16777215, 30))
        self.label_usbpdsink_sourcecaps.setFont(font1)
        self.label_usbpdsink_sourcecaps.setCursor(QCursor(Qt.UpArrowCursor))
        self.label_usbpdsink_sourcecaps.setStyleSheet(u"border:none;")
        self.label_usbpdsink_sourcecaps.setAlignment(Qt.AlignCenter)

        self.verticalLayout_33.addWidget(self.label_usbpdsink_sourcecaps)

        self.list_usbpdsink_sourcecaps = QListWidget(self.frame_5)
        QListWidgetItem(self.list_usbpdsink_sourcecaps)
        QListWidgetItem(self.list_usbpdsink_sourcecaps)
        QListWidgetItem(self.list_usbpdsink_sourcecaps)
        QListWidgetItem(self.list_usbpdsink_sourcecaps)
        QListWidgetItem(self.list_usbpdsink_sourcecaps)
        QListWidgetItem(self.list_usbpdsink_sourcecaps)
        QListWidgetItem(self.list_usbpdsink_sourcecaps)
        QListWidgetItem(self.list_usbpdsink_sourcecaps)
        QListWidgetItem(self.list_usbpdsink_sourcecaps)
        QListWidgetItem(self.list_usbpdsink_sourcecaps)
        QListWidgetItem(self.list_usbpdsink_sourcecaps)
        QListWidgetItem(self.list_usbpdsink_sourcecaps)
        QListWidgetItem(self.list_usbpdsink_sourcecaps)
        self.list_usbpdsink_sourcecaps.setObjectName(u"list_usbpdsink_sourcecaps")
        font11 = QFont()
        font11.setFamily(u"Consolas")
        font11.setPointSize(10)
        self.list_usbpdsink_sourcecaps.setFont(font11)
        self.list_usbpdsink_sourcecaps.setStyleSheet(u"background-color: rgb(19,24, 34);")

        self.verticalLayout_33.addWidget(self.list_usbpdsink_sourcecaps)

        self.btn_usbpdsink_request = QPushButton(self.frame_5)
        self.btn_usbpdsink_request.setObjectName(u"btn_usbpdsink_request")
        self.btn_usbpdsink_request.setFont(font2)
        self.btn_usbpdsink_request.setStyleSheet(u"QPushButton {\n"
"	border: 2px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(57, 65, 80);\n"
"	border: 2px solid rgb(61, 70, 86);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(35, 40, 49);\n"
"	border: 2px solid rgb(43, 50, 61);\n"
"}")

        self.verticalLayout_33.addWidget(self.btn_usbpdsink_request)


        self.horizontalLayout_16.addWidget(self.frame_5)

        self.frame_4 = QFrame(self.frame_usb_pd_sink_contents)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.verticalLayout_34 = QVBoxLayout(self.frame_4)
        self.verticalLayout_34.setObjectName(u"verticalLayout_34")
        self.label_usbpdsink_request_params = QLabel(self.frame_4)
        self.label_usbpdsink_request_params.setObjectName(u"label_usbpdsink_request_params")
        self.label_usbpdsink_request_params.setMaximumSize(QSize(16777215, 30))
        font12 = QFont()
        font12.setFamily(u"Segoe UI")
        font12.setPointSize(12)
        font12.setBold(True)
        font12.setWeight(75)
        self.label_usbpdsink_request_params.setFont(font12)
        self.label_usbpdsink_request_params.setCursor(QCursor(Qt.UpArrowCursor))
        self.label_usbpdsink_request_params.setStyleSheet(u"border:none;")
        self.label_usbpdsink_request_params.setAlignment(Qt.AlignCenter)

        self.verticalLayout_34.addWidget(self.label_usbpdsink_request_params)

        self.label_usbpdsink_request_param1 = QLabel(self.frame_4)
        self.label_usbpdsink_request_param1.setObjectName(u"label_usbpdsink_request_param1")
        self.label_usbpdsink_request_param1.setMaximumSize(QSize(16777215, 30))
        self.label_usbpdsink_request_param1.setFont(font2)
        self.label_usbpdsink_request_param1.setStyleSheet(u"border-radius: 0px;")

        self.verticalLayout_34.addWidget(self.label_usbpdsink_request_param1)

        self.lineedit_manual_usbpd_request_param1 = QLineEdit(self.frame_4)
        self.lineedit_manual_usbpd_request_param1.setObjectName(u"lineedit_manual_usbpd_request_param1")
        self.lineedit_manual_usbpd_request_param1.setFont(font3)
        self.lineedit_manual_usbpd_request_param1.setStyleSheet(u"border: 1px solid black;\n"
"border-radius: 0px;\n"
"background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")

        self.verticalLayout_34.addWidget(self.lineedit_manual_usbpd_request_param1)

        self.label_usbpdsink_request_param2 = QLabel(self.frame_4)
        self.label_usbpdsink_request_param2.setObjectName(u"label_usbpdsink_request_param2")
        self.label_usbpdsink_request_param2.setMinimumSize(QSize(0, 30))
        self.label_usbpdsink_request_param2.setMaximumSize(QSize(16777215, 30))
        self.label_usbpdsink_request_param2.setFont(font2)
        self.label_usbpdsink_request_param2.setStyleSheet(u"border-radius: 0px;")

        self.verticalLayout_34.addWidget(self.label_usbpdsink_request_param2)

        self.lineedit_manual_usbpd_request_param2 = QLineEdit(self.frame_4)
        self.lineedit_manual_usbpd_request_param2.setObjectName(u"lineedit_manual_usbpd_request_param2")
        self.lineedit_manual_usbpd_request_param2.setFont(font2)
        self.lineedit_manual_usbpd_request_param2.setStyleSheet(u"border: 1px solid black;\n"
"border-radius: 0px;\n"
"background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")

        self.verticalLayout_34.addWidget(self.lineedit_manual_usbpd_request_param2)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_34.addItem(self.verticalSpacer)


        self.horizontalLayout_16.addWidget(self.frame_4)


        self.verticalLayout_22.addWidget(self.frame_usb_pd_sink_contents)


        self.horizontalLayout_13.addWidget(self.frame_usb_pd_sink)


        self.verticalLayout_12.addWidget(self.frame_manual_control_lower)

        self.stackedWidget.addWidget(self.page_manual_control)
        self.page_add_tests = QWidget()
        self.page_add_tests.setObjectName(u"page_add_tests")
        self.stackedWidget.addWidget(self.page_add_tests)
        self.page_test_list = QWidget()
        self.page_test_list.setObjectName(u"page_test_list")
        self.stackedWidget.addWidget(self.page_test_list)
        self.page_view_logs = QWidget()
        self.page_view_logs.setObjectName(u"page_view_logs")
        self.stackedWidget.addWidget(self.page_view_logs)
        self.page_save_load_configs = QWidget()
        self.page_save_load_configs.setObjectName(u"page_save_load_configs")
        self.stackedWidget.addWidget(self.page_save_load_configs)
        self.page_settings = QWidget()
        self.page_settings.setObjectName(u"page_settings")
        self.stackedWidget.addWidget(self.page_settings)
        self.page_widgets = QWidget()
        self.page_widgets.setObjectName(u"page_widgets")
        self.verticalLayout_6 = QVBoxLayout(self.page_widgets)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.frame = QFrame(self.page_widgets)
        self.frame.setObjectName(u"frame")
        self.frame.setStyleSheet(u"border-radius: 5px;")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_15 = QVBoxLayout(self.frame)
        self.verticalLayout_15.setSpacing(0)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.verticalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.frame_div_content_1 = QFrame(self.frame)
        self.frame_div_content_1.setObjectName(u"frame_div_content_1")
        self.frame_div_content_1.setMinimumSize(QSize(0, 110))
        self.frame_div_content_1.setMaximumSize(QSize(16777215, 110))
        self.frame_div_content_1.setStyleSheet(u"background-color: rgb(41, 45, 56);\n"
"border-radius: 5px;\n"
"")
        self.frame_div_content_1.setFrameShape(QFrame.NoFrame)
        self.frame_div_content_1.setFrameShadow(QFrame.Raised)
        self.verticalLayout_7 = QVBoxLayout(self.frame_div_content_1)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.frame_title_wid_1 = QFrame(self.frame_div_content_1)
        self.frame_title_wid_1.setObjectName(u"frame_title_wid_1")
        self.frame_title_wid_1.setMaximumSize(QSize(16777215, 35))
        self.frame_title_wid_1.setStyleSheet(u"background-color: rgb(39, 44, 54);")
        self.frame_title_wid_1.setFrameShape(QFrame.StyledPanel)
        self.frame_title_wid_1.setFrameShadow(QFrame.Raised)
        self.verticalLayout_8 = QVBoxLayout(self.frame_title_wid_1)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.labelBoxBlenderInstalation = QLabel(self.frame_title_wid_1)
        self.labelBoxBlenderInstalation.setObjectName(u"labelBoxBlenderInstalation")
        self.labelBoxBlenderInstalation.setFont(font1)
        self.labelBoxBlenderInstalation.setStyleSheet(u"")

        self.verticalLayout_8.addWidget(self.labelBoxBlenderInstalation)


        self.verticalLayout_7.addWidget(self.frame_title_wid_1)

        self.frame_content_wid_1 = QFrame(self.frame_div_content_1)
        self.frame_content_wid_1.setObjectName(u"frame_content_wid_1")
        self.frame_content_wid_1.setFrameShape(QFrame.NoFrame)
        self.frame_content_wid_1.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_9 = QHBoxLayout(self.frame_content_wid_1)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(-1, -1, -1, 0)
        self.lineEdit = QLineEdit(self.frame_content_wid_1)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setMinimumSize(QSize(0, 30))
        self.lineEdit.setStyleSheet(u"QLineEdit {\n"
"	background-color: rgb(27, 29, 35);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(27, 29, 35);\n"
"	padding-left: 10px;\n"
"}\n"
"QLineEdit:hover {\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QLineEdit:focus {\n"
"	border: 2px solid rgb(91, 101, 124);\n"
"}")

        self.gridLayout.addWidget(self.lineEdit, 0, 0, 1, 1)

        self.pushButton = QPushButton(self.frame_content_wid_1)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setMinimumSize(QSize(150, 30))
        font13 = QFont()
        font13.setFamily(u"Segoe UI")
        font13.setPointSize(9)
        self.pushButton.setFont(font13)
        self.pushButton.setStyleSheet(u"QPushButton {\n"
"	border: 2px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(57, 65, 80);\n"
"	border: 2px solid rgb(61, 70, 86);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(35, 40, 49);\n"
"	border: 2px solid rgb(43, 50, 61);\n"
"}")
        icon3 = QIcon()
        icon3.addFile(u":/16x16/icons/16x16/cil-folder-open.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton.setIcon(icon3)

        self.gridLayout.addWidget(self.pushButton, 0, 1, 1, 1)

        self.labelVersion_3 = QLabel(self.frame_content_wid_1)
        self.labelVersion_3.setObjectName(u"labelVersion_3")
        self.labelVersion_3.setStyleSheet(u"color: rgb(98, 103, 111);")
        self.labelVersion_3.setLineWidth(1)
        self.labelVersion_3.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.labelVersion_3, 1, 0, 1, 2)


        self.horizontalLayout_9.addLayout(self.gridLayout)


        self.verticalLayout_7.addWidget(self.frame_content_wid_1)


        self.verticalLayout_15.addWidget(self.frame_div_content_1)


        self.verticalLayout_6.addWidget(self.frame)

        self.frame_2 = QFrame(self.page_widgets)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(0, 150))
        self.frame_2.setStyleSheet(u"background-color: rgb(39, 44, 54);\n"
"border-radius: 5px;")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.verticalLayout_11 = QVBoxLayout(self.frame_2)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.comboBox = QComboBox(self.frame_2)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setFont(font13)
        self.comboBox.setAutoFillBackground(False)
        self.comboBox.setStyleSheet(u"QComboBox{\n"
"	background-color: rgb(27, 29, 35);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(27, 29, 35);\n"
"	padding: 5px;\n"
"	padding-left: 10px;\n"
"}\n"
"QComboBox:hover{\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QComboBox QAbstractItemView {\n"
"	color: rgb(85, 170, 255);	\n"
"	background-color: rgb(27, 29, 35);\n"
"	padding: 10px;\n"
"	selection-background-color: rgb(39, 44, 54);\n"
"}")
        self.comboBox.setIconSize(QSize(16, 16))
        self.comboBox.setFrame(True)

        self.gridLayout_2.addWidget(self.comboBox, 1, 0, 1, 2)

        self.verticalSlider = QSlider(self.frame_2)
        self.verticalSlider.setObjectName(u"verticalSlider")
        self.verticalSlider.setStyleSheet(u"")
        self.verticalSlider.setOrientation(Qt.Vertical)

        self.gridLayout_2.addWidget(self.verticalSlider, 0, 2, 3, 1)

        self.scrollArea = QScrollArea(self.frame_2)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setStyleSheet(u"QScrollArea {\n"
"	border: none;\n"
"	border-radius: 0px;\n"
"}\n"
"QScrollBar:horizontal {\n"
"    border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    height: 14px;\n"
"    margin: 0px 21px 0 21px;\n"
"	border-radius: 0px;\n"
"}\n"
" QScrollBar:vertical {\n"
"	border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    width: 14px;\n"
"    margin: 21px 0 21px 0;\n"
"	border-radius: 0px;\n"
" }\n"
"")
        self.scrollArea.setFrameShape(QFrame.NoFrame)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 218, 218))
        self.horizontalLayout_11 = QHBoxLayout(self.scrollAreaWidgetContents)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.plainTextEdit = QPlainTextEdit(self.scrollAreaWidgetContents)
        self.plainTextEdit.setObjectName(u"plainTextEdit")
        self.plainTextEdit.setMinimumSize(QSize(200, 200))
        self.plainTextEdit.setStyleSheet(u"QPlainTextEdit {\n"
"	background-color: rgb(27, 29, 35);\n"
"	border-radius: 5px;\n"
"	padding: 10px;\n"
"}\n"
"QPlainTextEdit:hover {\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QPlainTextEdit:focus {\n"
"	border: 2px solid rgb(91, 101, 124);\n"
"}")

        self.horizontalLayout_11.addWidget(self.plainTextEdit)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout_2.addWidget(self.scrollArea, 0, 5, 3, 1)

        self.horizontalScrollBar = QScrollBar(self.frame_2)
        self.horizontalScrollBar.setObjectName(u"horizontalScrollBar")
        sizePolicy7 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.horizontalScrollBar.sizePolicy().hasHeightForWidth())
        self.horizontalScrollBar.setSizePolicy(sizePolicy7)
        self.horizontalScrollBar.setStyleSheet(u"QScrollBar:horizontal {\n"
"    border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    height: 14px;\n"
"    margin: 0px 21px 0 21px;\n"
"	border-radius: 0px;\n"
"}\n"
"")
        self.horizontalScrollBar.setOrientation(Qt.Horizontal)

        self.gridLayout_2.addWidget(self.horizontalScrollBar, 1, 3, 1, 1)

        self.verticalScrollBar = QScrollBar(self.frame_2)
        self.verticalScrollBar.setObjectName(u"verticalScrollBar")
        self.verticalScrollBar.setStyleSheet(u" QScrollBar:vertical {\n"
"	border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    width: 14px;\n"
"    margin: 21px 0 21px 0;\n"
"	border-radius: 0px;\n"
" }")
        self.verticalScrollBar.setOrientation(Qt.Vertical)

        self.gridLayout_2.addWidget(self.verticalScrollBar, 0, 4, 3, 1)

        self.commandLinkButton = QCommandLinkButton(self.frame_2)
        self.commandLinkButton.setObjectName(u"commandLinkButton")
        self.commandLinkButton.setStyleSheet(u"QCommandLinkButton {	\n"
"	color: rgb(85, 170, 255);\n"
"	border-radius: 5px;\n"
"	padding: 5px;\n"
"}\n"
"QCommandLinkButton:hover {	\n"
"	color: rgb(210, 210, 210);\n"
"	background-color: rgb(44, 49, 60);\n"
"}\n"
"QCommandLinkButton:pressed {	\n"
"	color: rgb(210, 210, 210);\n"
"	background-color: rgb(52, 58, 71);\n"
"}")
        icon4 = QIcon()
        icon4.addFile(u":/16x16/icons/16x16/cil-link.png", QSize(), QIcon.Normal, QIcon.Off)
        self.commandLinkButton.setIcon(icon4)

        self.gridLayout_2.addWidget(self.commandLinkButton, 1, 6, 1, 1)

        self.checkBox = QCheckBox(self.frame_2)
        self.checkBox.setObjectName(u"checkBox")
        self.checkBox.setAutoFillBackground(False)
        self.checkBox.setStyleSheet(u"")

        self.gridLayout_2.addWidget(self.checkBox, 0, 0, 1, 1)

        self.radioButton = QRadioButton(self.frame_2)
        self.radioButton.setObjectName(u"radioButton")
        self.radioButton.setStyleSheet(u"")

        self.gridLayout_2.addWidget(self.radioButton, 0, 1, 1, 1)

        self.horizontalSlider = QSlider(self.frame_2)
        self.horizontalSlider.setObjectName(u"horizontalSlider")
        self.horizontalSlider.setStyleSheet(u"")
        self.horizontalSlider.setOrientation(Qt.Horizontal)

        self.gridLayout_2.addWidget(self.horizontalSlider, 2, 0, 1, 2)


        self.verticalLayout_11.addLayout(self.gridLayout_2)


        self.verticalLayout_6.addWidget(self.frame_2)

        self.frame_3 = QFrame(self.page_widgets)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(0, 150))
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_12 = QHBoxLayout(self.frame_3)
        self.horizontalLayout_12.setSpacing(0)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.tableWidget = QTableWidget(self.frame_3)
        if (self.tableWidget.columnCount() < 4):
            self.tableWidget.setColumnCount(4)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        if (self.tableWidget.rowCount() < 16):
            self.tableWidget.setRowCount(16)
        font14 = QFont()
        font14.setFamily(u"Segoe UI")
        __qtablewidgetitem4 = QTableWidgetItem()
        __qtablewidgetitem4.setFont(font14);
        self.tableWidget.setVerticalHeaderItem(0, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(1, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(2, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(3, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(4, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(5, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(6, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(7, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(8, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(9, __qtablewidgetitem13)
        __qtablewidgetitem14 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(10, __qtablewidgetitem14)
        __qtablewidgetitem15 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(11, __qtablewidgetitem15)
        __qtablewidgetitem16 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(12, __qtablewidgetitem16)
        __qtablewidgetitem17 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(13, __qtablewidgetitem17)
        __qtablewidgetitem18 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(14, __qtablewidgetitem18)
        __qtablewidgetitem19 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(15, __qtablewidgetitem19)
        __qtablewidgetitem20 = QTableWidgetItem()
        self.tableWidget.setItem(0, 0, __qtablewidgetitem20)
        __qtablewidgetitem21 = QTableWidgetItem()
        self.tableWidget.setItem(0, 1, __qtablewidgetitem21)
        __qtablewidgetitem22 = QTableWidgetItem()
        self.tableWidget.setItem(0, 2, __qtablewidgetitem22)
        __qtablewidgetitem23 = QTableWidgetItem()
        self.tableWidget.setItem(0, 3, __qtablewidgetitem23)
        self.tableWidget.setObjectName(u"tableWidget")
        sizePolicy.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy)
        palette1 = QPalette()
        palette1.setBrush(QPalette.Active, QPalette.WindowText, brush6)
        brush12 = QBrush(QColor(39, 44, 54, 255))
        brush12.setStyle(Qt.SolidPattern)
        palette1.setBrush(QPalette.Active, QPalette.Button, brush12)
        palette1.setBrush(QPalette.Active, QPalette.Text, brush6)
        palette1.setBrush(QPalette.Active, QPalette.ButtonText, brush6)
        palette1.setBrush(QPalette.Active, QPalette.Base, brush12)
        palette1.setBrush(QPalette.Active, QPalette.Window, brush12)
        palette1.setBrush(QPalette.Inactive, QPalette.WindowText, brush6)
        palette1.setBrush(QPalette.Inactive, QPalette.Button, brush12)
        palette1.setBrush(QPalette.Inactive, QPalette.Text, brush6)
        palette1.setBrush(QPalette.Inactive, QPalette.ButtonText, brush6)
        palette1.setBrush(QPalette.Inactive, QPalette.Base, brush12)
        palette1.setBrush(QPalette.Inactive, QPalette.Window, brush12)
        palette1.setBrush(QPalette.Disabled, QPalette.WindowText, brush6)
        palette1.setBrush(QPalette.Disabled, QPalette.Button, brush12)
        palette1.setBrush(QPalette.Disabled, QPalette.Text, brush6)
        palette1.setBrush(QPalette.Disabled, QPalette.ButtonText, brush6)
        palette1.setBrush(QPalette.Disabled, QPalette.Base, brush12)
        palette1.setBrush(QPalette.Disabled, QPalette.Window, brush12)
        self.tableWidget.setPalette(palette1)
        self.tableWidget.setStyleSheet(u"QTableWidget {	\n"
"	background-color: rgb(39, 44, 54);\n"
"	padding: 10px;\n"
"	border-radius: 5px;\n"
"	gridline-color: rgb(44, 49, 60);\n"
"	border-bottom: 1px solid rgb(44, 49, 60);\n"
"}\n"
"QTableWidget::item{\n"
"	border-color: rgb(44, 49, 60);\n"
"	padding-left: 5px;\n"
"	padding-right: 5px;\n"
"	gridline-color: rgb(44, 49, 60);\n"
"}\n"
"QTableWidget::item:selected{\n"
"	background-color: rgb(85, 170, 255);\n"
"}\n"
"QScrollBar:horizontal {\n"
"    border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    height: 14px;\n"
"    margin: 0px 21px 0 21px;\n"
"	border-radius: 0px;\n"
"}\n"
" QScrollBar:vertical {\n"
"	border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    width: 14px;\n"
"    margin: 21px 0 21px 0;\n"
"	border-radius: 0px;\n"
" }\n"
"QHeaderView::section{\n"
"	Background-color: rgb(39, 44, 54);\n"
"	max-width: 30px;\n"
"	border: 1px solid rgb(44, 49, 60);\n"
"	border-style: none;\n"
"    border-bottom: 1px solid rgb(44, 49, 60);\n"
"    border-right: 1px solid rgb(44, 49, 60);\n"
"}\n"
""
                        "QTableWidget::horizontalHeader {	\n"
"	background-color: rgb(81, 255, 0);\n"
"}\n"
"QHeaderView::section:horizontal\n"
"{\n"
"    border: 1px solid rgb(32, 34, 42);\n"
"	background-color: rgb(27, 29, 35);\n"
"	padding: 3px;\n"
"	border-top-left-radius: 7px;\n"
"    border-top-right-radius: 7px;\n"
"}\n"
"QHeaderView::section:vertical\n"
"{\n"
"    border: 1px solid rgb(44, 49, 60);\n"
"}\n"
"")
        self.tableWidget.setFrameShape(QFrame.NoFrame)
        self.tableWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.tableWidget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setAlternatingRowColors(False)
        self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.setShowGrid(True)
        self.tableWidget.setGridStyle(Qt.SolidLine)
        self.tableWidget.setSortingEnabled(False)
        self.tableWidget.horizontalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(True)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(200)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget.verticalHeader().setHighlightSections(False)
        self.tableWidget.verticalHeader().setStretchLastSection(True)

        self.horizontalLayout_12.addWidget(self.tableWidget)


        self.verticalLayout_6.addWidget(self.frame_3)

        self.stackedWidget.addWidget(self.page_widgets)

        self.verticalLayout_9.addWidget(self.stackedWidget)


        self.verticalLayout_4.addWidget(self.frame_content)

        self.frame_grip = QFrame(self.frame_content_right)
        self.frame_grip.setObjectName(u"frame_grip")
        self.frame_grip.setMinimumSize(QSize(0, 25))
        self.frame_grip.setMaximumSize(QSize(16777215, 25))
        self.frame_grip.setStyleSheet(u"background-color: rgb(33, 37, 43);")
        self.frame_grip.setFrameShape(QFrame.NoFrame)
        self.frame_grip.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.frame_grip)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 2, 0)
        self.frame_label_bottom = QFrame(self.frame_grip)
        self.frame_label_bottom.setObjectName(u"frame_label_bottom")
        self.frame_label_bottom.setFrameShape(QFrame.NoFrame)
        self.frame_label_bottom.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_7 = QHBoxLayout(self.frame_label_bottom)
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(10, 0, 10, 0)
        self.label_credits = QLabel(self.frame_label_bottom)
        self.label_credits.setObjectName(u"label_credits")
        self.label_credits.setFont(font14)
        self.label_credits.setStyleSheet(u"color: rgb(98, 103, 111);")

        self.horizontalLayout_7.addWidget(self.label_credits)

        self.label_version = QLabel(self.frame_label_bottom)
        self.label_version.setObjectName(u"label_version")
        self.label_version.setMaximumSize(QSize(100, 16777215))
        self.label_version.setFont(font14)
        self.label_version.setStyleSheet(u"color: rgb(98, 103, 111);")
        self.label_version.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_7.addWidget(self.label_version)


        self.horizontalLayout_6.addWidget(self.frame_label_bottom)

        self.frame_size_grip = QFrame(self.frame_grip)
        self.frame_size_grip.setObjectName(u"frame_size_grip")
        self.frame_size_grip.setMaximumSize(QSize(20, 20))
        self.frame_size_grip.setStyleSheet(u"QSizeGrip {\n"
"	background-image: url(:/16x16/icons/16x16/cil-size-grip.png);\n"
"	background-position: center;\n"
"	background-repeat: no-reperat;\n"
"}")
        self.frame_size_grip.setFrameShape(QFrame.NoFrame)
        self.frame_size_grip.setFrameShadow(QFrame.Raised)

        self.horizontalLayout_6.addWidget(self.frame_size_grip)


        self.verticalLayout_4.addWidget(self.frame_grip)


        self.horizontalLayout_2.addWidget(self.frame_content_right)


        self.verticalLayout.addWidget(self.frame_center)


        self.verticalLayout_13.addWidget(self.frame_main)

        MainWindow.setCentralWidget(self.centralwidget)
        QWidget.setTabOrder(self.btn_minimize, self.btn_maximize_restore)
        QWidget.setTabOrder(self.btn_maximize_restore, self.btn_close)
        QWidget.setTabOrder(self.btn_close, self.btn_toggle_menu)
        QWidget.setTabOrder(self.btn_toggle_menu, self.checkBox)
        QWidget.setTabOrder(self.checkBox, self.comboBox)
        QWidget.setTabOrder(self.comboBox, self.radioButton)
        QWidget.setTabOrder(self.radioButton, self.horizontalSlider)
        QWidget.setTabOrder(self.horizontalSlider, self.verticalSlider)
        QWidget.setTabOrder(self.verticalSlider, self.scrollArea)
        QWidget.setTabOrder(self.scrollArea, self.plainTextEdit)
        QWidget.setTabOrder(self.plainTextEdit, self.tableWidget)
        QWidget.setTabOrder(self.tableWidget, self.commandLinkButton)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(2)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.btn_toggle_menu.setText("")
        self.label_title_bar_top.setText(QCoreApplication.translate("MainWindow", u"Main Window - Base", None))
#if QT_CONFIG(tooltip)
        self.btn_minimize.setToolTip(QCoreApplication.translate("MainWindow", u"Minimize", None))
#endif // QT_CONFIG(tooltip)
        self.btn_minimize.setText("")
#if QT_CONFIG(tooltip)
        self.btn_maximize_restore.setToolTip(QCoreApplication.translate("MainWindow", u"Maximize", None))
#endif // QT_CONFIG(tooltip)
        self.btn_maximize_restore.setText("")
#if QT_CONFIG(tooltip)
        self.btn_close.setToolTip(QCoreApplication.translate("MainWindow", u"Close", None))
#endif // QT_CONFIG(tooltip)
        self.btn_close.setText("")
        self.label_top_info_1.setText(QCoreApplication.translate("MainWindow", u"Power Integrations", None))
        self.label_top_info_2.setText(QCoreApplication.translate("MainWindow", u"| HOME", None))
        self.label_user_icon.setText(QCoreApplication.translate("MainWindow", u"PI", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"PI ATE", None))
        self.label.setText("")
        self.label_7.setText("")
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"MANUAL EQUIPMENT CONTROL", None))
        self.label_source_power_meter.setText(QCoreApplication.translate("MainWindow", u"SOURCE POWER METER", None))
        self.label_pms_display_a.setText(QCoreApplication.translate("MainWindow", u"230.54 V", None))
        self.label_pms_display_b.setText(QCoreApplication.translate("MainWindow", u"10.635 A", None))
        self.label_pms_display_c.setText(QCoreApplication.translate("MainWindow", u"2451.7 W", None))
        self.label_pms_display_d.setText(QCoreApplication.translate("MainWindow", u"0.9937  ", None))
        self.label_pms_voltage_range.setText(QCoreApplication.translate("MainWindow", u"Voltage Range", None))
        self.cbx_pms_voltage_range.setItemText(0, QCoreApplication.translate("MainWindow", u"AUTO", None))
        self.cbx_pms_voltage_range.setItemText(1, QCoreApplication.translate("MainWindow", u"10 mA", None))

        self.label_pms_current_range.setText(QCoreApplication.translate("MainWindow", u"Current Range", None))
        self.cbx_pms_current_range.setItemText(0, QCoreApplication.translate("MainWindow", u"AUTO", None))
        self.cbx_pms_current_range.setItemText(1, QCoreApplication.translate("MainWindow", u"10 mA", None))

        self.label_pms_integration.setText(QCoreApplication.translate("MainWindow", u"Integration", None))
        self.btn_pms_integration_start.setText(QCoreApplication.translate("MainWindow", u"START", None))
        self.btn_pms_integration_stop.setText(QCoreApplication.translate("MainWindow", u"STOP", None))
        self.btn_pms_integration_reset.setText(QCoreApplication.translate("MainWindow", u"RESET", None))
        self.label_pms_averaging.setText(QCoreApplication.translate("MainWindow", u"Averaging", None))
        self.btn_pms_averaging_toggle.setText(QCoreApplication.translate("MainWindow", u"OFF", None))
        self.cbx_pms_averaging_count.setItemText(0, QCoreApplication.translate("MainWindow", u"8", None))
        self.cbx_pms_averaging_count.setItemText(1, QCoreApplication.translate("MainWindow", u"16", None))
        self.cbx_pms_averaging_count.setItemText(2, QCoreApplication.translate("MainWindow", u"64", None))

        self.cbx_pms_averaging_mode.setItemText(0, QCoreApplication.translate("MainWindow", u"LIN", None))
        self.cbx_pms_averaging_mode.setItemText(1, QCoreApplication.translate("MainWindow", u"EXP", None))

        self.label_pms_measure_mode.setText(QCoreApplication.translate("MainWindow", u"Mode", None))
        self.btn_pms_measure_mode.setText(QCoreApplication.translate("MainWindow", u"RMS", None))
        self.label_source_power_meter_2.setText(QCoreApplication.translate("MainWindow", u"LOAD POWER METER", None))
        self.label_pml_display_a.setText(QCoreApplication.translate("MainWindow", u"230.54 V", None))
        self.label_pml_display_b.setText(QCoreApplication.translate("MainWindow", u"10.635 A", None))
        self.label_pml_display_c.setText(QCoreApplication.translate("MainWindow", u"2451.7 W", None))
        self.label_pml_display_d.setText(QCoreApplication.translate("MainWindow", u"0.9937  ", None))
        self.label_pms_voltage_range_2.setText(QCoreApplication.translate("MainWindow", u"Voltage Range", None))
        self.cbx_pms_voltage_range_2.setItemText(0, QCoreApplication.translate("MainWindow", u"AUTO", None))
        self.cbx_pms_voltage_range_2.setItemText(1, QCoreApplication.translate("MainWindow", u"10 mA", None))

        self.label_pms_current_range_2.setText(QCoreApplication.translate("MainWindow", u"Current Range", None))
        self.cbx_pms_current_range_2.setItemText(0, QCoreApplication.translate("MainWindow", u"AUTO", None))
        self.cbx_pms_current_range_2.setItemText(1, QCoreApplication.translate("MainWindow", u"10 mA", None))

        self.label_pms_integration_2.setText(QCoreApplication.translate("MainWindow", u"Integration", None))
        self.btn_pms_integration_start_2.setText(QCoreApplication.translate("MainWindow", u"START", None))
        self.btn_pms_integration_stop_2.setText(QCoreApplication.translate("MainWindow", u"STOP", None))
        self.btn_pms_integration_reset_2.setText(QCoreApplication.translate("MainWindow", u"RESET", None))
        self.label_pms_averaging_2.setText(QCoreApplication.translate("MainWindow", u"Averaging", None))
        self.btn_pms_averaging_toggle_2.setText(QCoreApplication.translate("MainWindow", u"OFF", None))
        self.cbx_pms_averaging_count_2.setItemText(0, QCoreApplication.translate("MainWindow", u"8", None))
        self.cbx_pms_averaging_count_2.setItemText(1, QCoreApplication.translate("MainWindow", u"16", None))
        self.cbx_pms_averaging_count_2.setItemText(2, QCoreApplication.translate("MainWindow", u"64", None))

        self.cbx_pml_averaging_mode.setItemText(0, QCoreApplication.translate("MainWindow", u"LIN", None))
        self.cbx_pml_averaging_mode.setItemText(1, QCoreApplication.translate("MainWindow", u"EXP", None))

        self.label_pms_measure_mode_2.setText(QCoreApplication.translate("MainWindow", u"Mode", None))
        self.btn_pms_measure_mode_2.setText(QCoreApplication.translate("MainWindow", u"RMS", None))
        self.label_source_ac_source.setText(QCoreApplication.translate("MainWindow", u"AC SOURCE", None))
        self.label_eload.setText(QCoreApplication.translate("MainWindow", u"ELECTRONIC LOAD", None))
        self.label_source_power_meter_5.setText(QCoreApplication.translate("MainWindow", u"USB PD SINK", None))
        self.label_usbpdsink_sourcecaps.setText(QCoreApplication.translate("MainWindow", u"SOURCE CAPABILITIES", None))

        __sortingEnabled = self.list_usbpdsink_sourcecaps.isSortingEnabled()
        self.list_usbpdsink_sourcecaps.setSortingEnabled(False)
        ___qlistwidgetitem = self.list_usbpdsink_sourcecaps.item(0)
        ___qlistwidgetitem.setText(QCoreApplication.translate("MainWindow", u"PDO 01: FPDO   5.0 V 3.0 A", None));
        ___qlistwidgetitem1 = self.list_usbpdsink_sourcecaps.item(1)
        ___qlistwidgetitem1.setText(QCoreApplication.translate("MainWindow", u"New Item", None));
        ___qlistwidgetitem2 = self.list_usbpdsink_sourcecaps.item(2)
        ___qlistwidgetitem2.setText(QCoreApplication.translate("MainWindow", u"New Item", None));
        ___qlistwidgetitem3 = self.list_usbpdsink_sourcecaps.item(3)
        ___qlistwidgetitem3.setText(QCoreApplication.translate("MainWindow", u"New Item", None));
        ___qlistwidgetitem4 = self.list_usbpdsink_sourcecaps.item(4)
        ___qlistwidgetitem4.setText(QCoreApplication.translate("MainWindow", u"New Item", None));
        ___qlistwidgetitem5 = self.list_usbpdsink_sourcecaps.item(5)
        ___qlistwidgetitem5.setText(QCoreApplication.translate("MainWindow", u"New Item", None));
        ___qlistwidgetitem6 = self.list_usbpdsink_sourcecaps.item(6)
        ___qlistwidgetitem6.setText(QCoreApplication.translate("MainWindow", u"New Item", None));
        ___qlistwidgetitem7 = self.list_usbpdsink_sourcecaps.item(7)
        ___qlistwidgetitem7.setText(QCoreApplication.translate("MainWindow", u"New Item", None));
        ___qlistwidgetitem8 = self.list_usbpdsink_sourcecaps.item(8)
        ___qlistwidgetitem8.setText(QCoreApplication.translate("MainWindow", u"New Item", None));
        ___qlistwidgetitem9 = self.list_usbpdsink_sourcecaps.item(9)
        ___qlistwidgetitem9.setText(QCoreApplication.translate("MainWindow", u"New Item", None));
        ___qlistwidgetitem10 = self.list_usbpdsink_sourcecaps.item(10)
        ___qlistwidgetitem10.setText(QCoreApplication.translate("MainWindow", u"New Item", None));
        ___qlistwidgetitem11 = self.list_usbpdsink_sourcecaps.item(11)
        ___qlistwidgetitem11.setText(QCoreApplication.translate("MainWindow", u"New Item", None));
        ___qlistwidgetitem12 = self.list_usbpdsink_sourcecaps.item(12)
        ___qlistwidgetitem12.setText(QCoreApplication.translate("MainWindow", u"PDO 13: AVS    15.0V to 48.0V 5A", None));
        self.list_usbpdsink_sourcecaps.setSortingEnabled(__sortingEnabled)

        self.btn_usbpdsink_request.setText(QCoreApplication.translate("MainWindow", u"REQUEST", None))
        self.label_usbpdsink_request_params.setText(QCoreApplication.translate("MainWindow", u"Request Parameters", None))
        self.label_usbpdsink_request_param1.setText(QCoreApplication.translate("MainWindow", u"Maximum Current (mA)", None))
        self.lineedit_manual_usbpd_request_param1.setText("")
        self.label_usbpdsink_request_param2.setText(QCoreApplication.translate("MainWindow", u"Operating Current (mA)", None))
        self.labelBoxBlenderInstalation.setText(QCoreApplication.translate("MainWindow", u"BLENDER INSTALLATION", None))
        self.lineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Your Password", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Open Blender", None))
        self.labelVersion_3.setText(QCoreApplication.translate("MainWindow", u"Ex: C:Program FilesBlender FoundationBlender 2.82 blender.exe", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"Test 1", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"Test 2", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"Test 3", None))

        self.commandLinkButton.setText(QCoreApplication.translate("MainWindow", u"CommandLinkButton", None))
        self.commandLinkButton.setDescription(QCoreApplication.translate("MainWindow", u"Open External Link", None))
        self.checkBox.setText(QCoreApplication.translate("MainWindow", u"CheckBox", None))
        self.radioButton.setText(QCoreApplication.translate("MainWindow", u"RadioButton", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"0", None));
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"1", None));
        ___qtablewidgetitem2 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"2", None));
        ___qtablewidgetitem3 = self.tableWidget.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"3", None));
        ___qtablewidgetitem4 = self.tableWidget.verticalHeaderItem(0)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem5 = self.tableWidget.verticalHeaderItem(1)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem6 = self.tableWidget.verticalHeaderItem(2)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem7 = self.tableWidget.verticalHeaderItem(3)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem8 = self.tableWidget.verticalHeaderItem(4)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem9 = self.tableWidget.verticalHeaderItem(5)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem10 = self.tableWidget.verticalHeaderItem(6)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem11 = self.tableWidget.verticalHeaderItem(7)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem12 = self.tableWidget.verticalHeaderItem(8)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem13 = self.tableWidget.verticalHeaderItem(9)
        ___qtablewidgetitem13.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem14 = self.tableWidget.verticalHeaderItem(10)
        ___qtablewidgetitem14.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem15 = self.tableWidget.verticalHeaderItem(11)
        ___qtablewidgetitem15.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem16 = self.tableWidget.verticalHeaderItem(12)
        ___qtablewidgetitem16.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem17 = self.tableWidget.verticalHeaderItem(13)
        ___qtablewidgetitem17.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem18 = self.tableWidget.verticalHeaderItem(14)
        ___qtablewidgetitem18.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem19 = self.tableWidget.verticalHeaderItem(15)
        ___qtablewidgetitem19.setText(QCoreApplication.translate("MainWindow", u"New Row", None));

        __sortingEnabled1 = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        ___qtablewidgetitem20 = self.tableWidget.item(0, 0)
        ___qtablewidgetitem20.setText(QCoreApplication.translate("MainWindow", u"Test", None));
        ___qtablewidgetitem21 = self.tableWidget.item(0, 1)
        ___qtablewidgetitem21.setText(QCoreApplication.translate("MainWindow", u"Text", None));
        ___qtablewidgetitem22 = self.tableWidget.item(0, 2)
        ___qtablewidgetitem22.setText(QCoreApplication.translate("MainWindow", u"Cell", None));
        ___qtablewidgetitem23 = self.tableWidget.item(0, 3)
        ___qtablewidgetitem23.setText(QCoreApplication.translate("MainWindow", u"Line", None));
        self.tableWidget.setSortingEnabled(__sortingEnabled1)

        self.label_credits.setText("")
        self.label_version.setText(QCoreApplication.translate("MainWindow", u"v1.0.0", None))
    # retranslateUi

