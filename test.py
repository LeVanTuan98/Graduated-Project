# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'notification_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(339, 273)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(90, 230, 161, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(9, 19, 321, 201))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.icon_lb = QtWidgets.QLabel(self.groupBox)
        self.icon_lb.setGeometry(QtCore.QRect(10, 10, 301, 181))
        self.icon_lb.setText("")
        self.icon_lb.setObjectName("icon_lb")
        self.icon_lb.setAlignment(QtCore.Qt.AlignCenter)

        icon = QtGui.QPixmap('Resourses/Icons/about.jpg')
        self.icon_lb.setPixmap(icon.scaled(self.icon_lb.size(), QtCore.Qt.KeepAspectRatio))

        self.text_lb = QtWidgets.QLabel(self.groupBox)
        self.text_lb.setGeometry(QtCore.QRect(30, 30, 261, 141))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.text_lb.setFont(font)
        self.text_lb.setText("hello world")
        self.text_lb.setObjectName("text_lb")

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

