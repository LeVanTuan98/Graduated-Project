# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'laserProcessGUI.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QImage
from pyqtgraph import PlotWidget
import numpy as np
from process import *
from sub_windows import *

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1081, 625)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setWindowIcon(QtGui.QIcon('Resourses/Icons/balance.svg'))

        #-------------------------Infomation Box-----------------------#
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 261, 371))
        self.groupBox.setObjectName("groupBox")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(20, 30, 91, 16))
        self.label.setObjectName("label")
        self.id_txt = QtWidgets.QLineEdit(self.groupBox)
        self.id_txt.setGeometry(QtCore.QRect(130, 30, 113, 20))
        self.id_txt.setObjectName("id_txt")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(20, 60, 91, 16))
        self.label_2.setObjectName("label_2")
        self.name_txt = QtWidgets.QLineEdit(self.groupBox)
        self.name_txt.setGeometry(QtCore.QRect(130, 60, 113, 20))
        self.name_txt.setObjectName("name_txt")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(20, 90, 91, 16))
        self.label_3.setObjectName("label_3")
        self.age_txt = QtWidgets.QLineEdit(self.groupBox)
        self.age_txt.setGeometry(QtCore.QRect(130, 90, 113, 20))
        self.age_txt.setObjectName("age_txt")
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setGeometry(QtCore.QRect(20, 120, 91, 21))
        self.label_4.setObjectName("label_4")
        self.sex_opt = QtWidgets.QComboBox(self.groupBox)
        self.sex_opt.setGeometry(QtCore.QRect(130, 120, 111, 22))
        self.sex_opt.setObjectName("sex_opt")
        self.sex_opt.addItem("")
        self.sex_opt.addItem("")
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setGeometry(QtCore.QRect(20, 150, 91, 21))
        self.label_5.setObjectName("label_5")
        self.height_txt = QtWidgets.QLineEdit(self.groupBox)
        self.height_txt.setGeometry(QtCore.QRect(130, 150, 113, 20))
        self.height_txt.setObjectName("height_txt")
        self.label_6 = QtWidgets.QLabel(self.groupBox)
        self.label_6.setGeometry(QtCore.QRect(20, 180, 91, 21))
        self.label_6.setObjectName("label_6")
        self.weight_txt = QtWidgets.QLineEdit(self.groupBox)
        self.weight_txt.setGeometry(QtCore.QRect(130, 180, 113, 20))
        self.weight_txt.setObjectName("weight_txt")
        self.add_txt = QtWidgets.QLineEdit(self.groupBox)
        self.add_txt.setGeometry(QtCore.QRect(20, 230, 221, 41))
        self.add_txt.setObjectName("add_txt")
        self.label_7 = QtWidgets.QLabel(self.groupBox)
        self.label_7.setGeometry(QtCore.QRect(20, 210, 91, 21))
        self.label_7.setObjectName("label_7")
        self.note_txt = QtWidgets.QLineEdit(self.groupBox)
        self.note_txt.setGeometry(QtCore.QRect(20, 300, 221, 51))
        self.note_txt.setObjectName("note_txt")
        self.label_8 = QtWidgets.QLabel(self.groupBox)
        self.label_8.setGeometry(QtCore.QRect(20, 270, 91, 21))
        self.label_8.setObjectName("label_8")

        #---------------------------Frame Box------------------------#
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(290, 10, 761, 431))
        self.groupBox_2.setObjectName("groupBox_2")
        self.scrollBar = QtWidgets.QScrollBar(self.groupBox_2)
        self.scrollBar.setGeometry(QtCore.QRect(10, 29, 20, 371))
        self.scrollBar.setOrientation(QtCore.Qt.Vertical)
        self.scrollBar.setObjectName("scrollBar")
        self.main_frame = MainFrame(self.groupBox_2)
        self.main_frame.setGeometry(QtCore.QRect(216, 20, 531, 381))
        self.main_frame.setText("")
        self.main_frame.setObjectName("main_frame")
        self.sub_frame1 = QtWidgets.QLabel(self.groupBox_2)
        self.sub_frame1.setGeometry(QtCore.QRect(50, 20, 141, 71))
        self.sub_frame1.setText("")
        self.sub_frame1.setObjectName("sub_frame1")
        self.sub_frame2 = QtWidgets.QLabel(self.groupBox_2)
        self.sub_frame2.setGeometry(QtCore.QRect(50, 110, 141, 71))
        self.sub_frame2.setText("")
        self.sub_frame2.setObjectName("sub_frame2")
        self.sub_frame3 = QtWidgets.QLabel(self.groupBox_2)
        self.sub_frame3.setGeometry(QtCore.QRect(50, 200, 141, 81))
        self.sub_frame3.setText("")
        self.sub_frame3.setObjectName("sub_frame3")
        self.sub_frame4 = QtWidgets.QLabel(self.groupBox_2)
        self.sub_frame4.setGeometry(QtCore.QRect(50, 300, 141, 81))
        self.sub_frame4.setText("")
        self.sub_frame4.setObjectName("sub_frame4")

        #---------------------------Control Panel----------------------#
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setGeometry(QtCore.QRect(10, 390, 261, 161))
        self.groupBox_3.setObjectName("groupBox_3")
        self.calib_btn = QtWidgets.QPushButton(self.groupBox_3)
        self.calib_btn.setGeometry(QtCore.QRect(20, 20, 61, 23))
        self.calib_btn.setObjectName("calib_btn")
        self.run_btn = QtWidgets.QPushButton(self.groupBox_3)
        self.run_btn.setGeometry(QtCore.QRect(20, 60, 61, 23))
        self.run_btn.setObjectName("run_btn")
        self.chart_rbtn = QtWidgets.QRadioButton(self.groupBox_3)
        self.chart_rbtn.setGeometry(QtCore.QRect(110, 20, 82, 17))
        self.chart_rbtn.setObjectName("chart_rbtn")
        self.progressBar = QtWidgets.QProgressBar(self.groupBox_3)
        self.progressBar.setGeometry(QtCore.QRect(100, 63, 151, 20))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")

        #--------------------------Console Box-----------------------#
        self.groupBox_4 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_4.setGeometry(QtCore.QRect(290, 439, 761, 111))
        self.groupBox_4.setObjectName("groupBox_4")
        self.console_list = QtWidgets.QListWidget(self.groupBox_4)
        self.console_list.setGeometry(QtCore.QRect(20, 20, 731, 81))
        self.console_list.setObjectName("console_list")

        #----------------------------Menu----------------------------#
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1081, 21))
        self.menubar.setObjectName("menubar")
        self.menu_File = QtWidgets.QMenu(self.menubar)
        self.menu_File.setObjectName("menu_File")
        self.menu_Open_Recent = QtWidgets.QMenu(self.menu_File)
        self.menu_Open_Recent.setObjectName("menu_Open_Recent")
        self.menu_Save_Options = QtWidgets.QMenu(self.menu_File)
        self.menu_Save_Options.setObjectName("menu_Save_Options")
        self.menu_Edit = QtWidgets.QMenu(self.menubar)
        self.menu_Edit.setObjectName("menu_Edit")
        self.menu_Help = QtWidgets.QMenu(self.menubar)
        self.menu_Help.setObjectName("menu_Help")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.action_New = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Resourses/Icons/new.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_New.setIcon(icon)
        self.action_New.setObjectName("action_New")
        self.action_Open = QtWidgets.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("Resourses/Icons/open.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_Open.setIcon(icon1)
        self.action_Open.setObjectName("action_Open")
        self.action_Save = QtWidgets.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("Resourses/Icons/save.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_Save.setIcon(icon2)
        self.action_Save.setObjectName("action_Save")
        self.action_Exit = QtWidgets.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("Resourses/Icons/exit.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_Exit.setIcon(icon3)
        self.action_Exit.setObjectName("action_Exit")
        self.action_Open_All = QtWidgets.QAction(MainWindow)
        self.action_Open_All.setObjectName("action_Open_All")
        self.action_Copy = QtWidgets.QAction(MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("Resourses/Icons/copy.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_Copy.setIcon(icon4)
        self.action_Copy.setObjectName("action_Copy")
        self.action_Paste = QtWidgets.QAction(MainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("Resourses/Icons/paste.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_Paste.setIcon(icon5)
        self.action_Paste.setObjectName("action_Paste")
        self.action_Cut = QtWidgets.QAction(MainWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("Resourses/Icons/cut.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_Cut.setIcon(icon6)
        self.action_Cut.setObjectName("action_Cut")
        self.action_File_and_Replace = QtWidgets.QAction(MainWindow)
        self.action_File_and_Replace.setObjectName("action_File_and_Replace")
        self.action_About = QtWidgets.QAction(MainWindow)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("Resourses/Icons/about.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_About.setIcon(icon7)
        self.action_About.setObjectName("action_About")
        self.action_Save_excel_file = QtWidgets.QAction(MainWindow)
        self.action_Save_excel_file.setObjectName("action_Save_excel_file")
        self.action_Save_chart = QtWidgets.QAction(MainWindow)
        self.action_Save_chart.setObjectName("action_Save_chart")
        self.action_Zoom_In = QtWidgets.QAction(MainWindow)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("Resourses/Icons/zoomin.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_Zoom_In.setIcon(icon8)
        self.action_Zoom_In.setObjectName("action_Zoom_In")
        self.action_Zoom_Out = QtWidgets.QAction(MainWindow)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap("Resourses/Icons/zoomout.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_Zoom_Out.setIcon(icon9)
        self.action_Zoom_Out.setObjectName("action_Zoom_Out")
        self.menu_Open_Recent.addAction(self.action_Open_All)
        self.menu_Save_Options.addAction(self.action_Save_excel_file)
        self.menu_Save_Options.addAction(self.action_Save_chart)
        self.menu_File.addAction(self.action_New)
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.action_Open)
        self.menu_File.addAction(self.menu_Open_Recent.menuAction())
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.action_Save)
        self.menu_File.addAction(self.menu_Save_Options.menuAction())
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.action_Exit)
        self.menu_Edit.addAction(self.action_Copy)
        self.menu_Edit.addAction(self.action_Paste)
        self.menu_Edit.addAction(self.action_Cut)
        self.menu_Edit.addSeparator()
        self.menu_Edit.addAction(self.action_Zoom_In)
        self.menu_Edit.addAction(self.action_Zoom_Out)
        self.menu_Edit.addSeparator()
        self.menu_Edit.addAction(self.action_File_and_Replace)
        self.menu_Help.addAction(self.action_About)
        self.menubar.addAction(self.menu_File.menuAction())
        self.menubar.addAction(self.menu_Edit.menuAction())
        self.menubar.addAction(self.menu_Help.menuAction())
        self.toolBar.addAction(self.action_New)
        self.toolBar.addAction(self.action_Open)
        self.toolBar.addAction(self.action_Save)
        self.toolBar.addAction(self.action_Exit)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.action_Zoom_In)
        self.toolBar.addAction(self.action_Zoom_Out)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.action_About)

        # --------------------------------Chart---------------------------------#
        self.graphicsView = PlotWidget(self.groupBox_2)
        self.graphicsView.setGeometry(QtCore.QRect(216, 20, 531, 381))
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.NoBrush)
        self.graphicsView.setBackgroundBrush(brush)
        self.graphicsView.setObjectName("graphicsView")
        self.graphicsView.setEnabled(True)
        self.graphicsView.setStyleSheet("background:white")

        self.graphicsView.setGeometry(QtCore.QRect(0, 0, 0, 0))


        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "RLTB"))
        self.groupBox.setTitle(_translate("MainWindow", "Information"))
        self.label.setText(_translate("MainWindow", "Patient\'s ID:"))
        self.label_2.setText(_translate("MainWindow", "Patient\'s Name:"))
        self.label_3.setText(_translate("MainWindow", "Patient\'s Age:"))
        self.label_4.setText(_translate("MainWindow", "Patient\'s Sex:"))
        self.sex_opt.setItemText(0, _translate("MainWindow", "Male"))
        self.sex_opt.setItemText(1, _translate("MainWindow", "Female"))
        self.label_5.setText(_translate("MainWindow", "Patient\'s Height:"))
        self.label_6.setText(_translate("MainWindow", "Patient\'s Weight:"))
        self.label_7.setText(_translate("MainWindow", "Patient\'s Address:"))
        self.label_8.setText(_translate("MainWindow", "Notes:"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Main Window"))
        self.groupBox_3.setTitle(_translate("MainWindow", "Control Panel"))
        self.calib_btn.setText(_translate("MainWindow", "Calibrate"))
        self.run_btn.setText(_translate("MainWindow", "Run..."))
        self.chart_rbtn.setText(_translate("MainWindow", "Show chart"))
        self.groupBox_4.setTitle(_translate("MainWindow", "Console Log"))
        self.menu_File.setTitle(_translate("MainWindow", "&File"))
        self.menu_Open_Recent.setTitle(_translate("MainWindow", "&Open Recent"))
        self.menu_Save_Options.setTitle(_translate("MainWindow", "&Save Options"))
        self.menu_Edit.setTitle(_translate("MainWindow", "&Edit"))
        self.menu_Help.setTitle(_translate("MainWindow", "&Help"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.action_New.setText(_translate("MainWindow", "&New..."))
        self.action_New.setToolTip(_translate("MainWindow", "Reset the current window"))
        self.action_New.setShortcut(_translate("MainWindow", "Ctrl+N"))
        self.action_Open.setText(_translate("MainWindow", "&Open..."))
        self.action_Open.setToolTip(_translate("MainWindow", "Open file to process"))
        self.action_Open.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.action_Save.setText(_translate("MainWindow", "&Save"))
        self.action_Save.setToolTip(_translate("MainWindow", "Save result"))
        self.action_Save.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.action_Exit.setText(_translate("MainWindow", "&Exit"))
        self.action_Exit.setToolTip(_translate("MainWindow", "Exit the window"))
        self.action_Exit.setShortcut(_translate("MainWindow", "Ctrl+E"))
        self.action_Open_All.setText(_translate("MainWindow", "&Open All"))
        self.action_Copy.setText(_translate("MainWindow", "&Copy"))
        self.action_Copy.setShortcut(_translate("MainWindow", "Ctrl+C"))
        self.action_Paste.setText(_translate("MainWindow", "&Paste"))
        self.action_Paste.setShortcut(_translate("MainWindow", "Ctrl+V"))
        self.action_Cut.setText(_translate("MainWindow", "&Cut"))
        self.action_Cut.setShortcut(_translate("MainWindow", "Ctrl+X"))
        self.action_File_and_Replace.setText(_translate("MainWindow", "&File and Replace..."))
        self.action_About.setText(_translate("MainWindow", "&About..."))
        self.action_Save_excel_file.setText(_translate("MainWindow", "&Save excel file"))
        self.action_Save_chart.setText(_translate("MainWindow", "&Save chart"))
        self.action_Zoom_In.setText(_translate("MainWindow", "&Zoom In"))
        self.action_Zoom_In.setShortcut(_translate("MainWindow", "Ctrl++"))
        self.action_Zoom_Out.setText(_translate("MainWindow", "&Zoom Out"))
        self.action_Zoom_Out.setShortcut(_translate("MainWindow", "Ctrl+-"))

        #----------------------------Control panel action----------------------------------#
        self.run_btn.clicked.connect(self.run_btn_clicked)
        self.calib_btn.clicked.connect(self.calib_btn_clicked)








    def show_sub_frame(self, frame1, frame2, frame3, frame4):
        self.sub_frame1.setPixmap(frame1.scaled(self.sub_frame1.size(), QtCore.Qt.KeepAspectRatio))
        self.sub_frame2.setPixmap(frame2.scaled(self.sub_frame2.size(), QtCore.Qt.KeepAspectRatio))
        self.sub_frame3.setPixmap(frame3.scaled(self.sub_frame3.size(), QtCore.Qt.KeepAspectRatio))
        self.sub_frame4.setPixmap(frame4.scaled(self.sub_frame4.size(), QtCore.Qt.KeepAspectRatio))

    def get_sub_frame(self, start_P):
        file_name = ""
        frame1 = QtGui.QPixmap("sample.jpg")
        frame2 = QtGui.QPixmap("sample.jpg")
        frame3 = QtGui.QPixmap("sample.jpg")
        frame4 = QtGui.QPixmap("sample.jpg")
        return frame1, frame2, frame3, frame4

    def is_chart(self):
        if self.chart_rbtn.isChecked():
            self.console_list.addItem("Chart radio button is being checked")
            self.graphicsView.setGeometry(QtCore.QRect(216, 20, 531, 381))
            return True
        else:
            self.console_list.addItem("Chart radio button is NOT being checked")
            self.graphicsView.setGeometry(QtCore.QRect(0, 0, 0, 0))
            return False

    def draw_graph(self):
        x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        y = [30, 32, 34, 32, 33, 31, 29, 32, 35, 45]
        self.graphicsView.plot(x, y)

    def clear_graph(self):
        self.graphicsView.clear()

    def show_chart(self):
        self.draw_graph()

    def run_btn_clicked(self):
        self.console_list.addItem("Blue color: " + str(self.main_frame.blueHSV))
        self.console_list.addItem("Laser color: " + str(self.main_frame.laserHSV))
        # print("Press RUN button")
        self.console_list.addItem("Press RUN button")
        if self.is_chart() == True:
            self.show_chart()
        else:
            print()

        frame1, frame2, frame3, frame4 = self.get_sub_frame(1)
        self.show_sub_frame(frame1, frame2, frame3, frame4)

    def calib_btn_clicked(self):
        # print("Press CALIBRATE button")
        self.console_list.addItem("Press CALIBRATE button")
        image = cv2.imread("sample.jpg")
        self.main_frame.show_main_frame(image)
        self.main_frame.is_laser = 0
        self.console_list.addItem("CHON 2 THONG SO MAU SAC TREN HINH")
        dlg = CustomDialog(message="CHON 2 THONG SO MAU SAC \r\n1. Chon thong so cho vung mau xanh \r\n2. Chon thong so cho vung laser")
        if not dlg.exec_():
            self.main_frame.setDisabled(True)





if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())



