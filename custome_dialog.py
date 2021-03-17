from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (
    QApplication,
    QDialog,
    QDialogButtonBox,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout, )



class CustomDialog(QDialog):
    def __init__(self, parent=None, title="Notification", type="noti", message=""):
        super().__init__(parent=parent)

        source_icon = 'Resourses/Icons/notification.svg'
        source_image = 'Resourses/Icons/noti.jpg'
        if type == 'alert':
            source_icon = 'Resourses/Icons/alert.svg'
            source_image = 'Resourses/Icons/alert.jpg'
        elif type == 'completed':
            source_icon = 'Resourses/Icons/completed.svg'
            source_image = 'Resourses/Icons/completed.jpg'
        self.setWindowTitle(title)
        self.setWindowIcon(QtGui.QIcon(source_icon))

        self.setObjectName("Dialog")
        self.resize(400, 212)
        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setGeometry(QtCore.QRect(40, 170, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.groupBox = QtWidgets.QGroupBox(self)
        self.groupBox.setGeometry(QtCore.QRect(9, 19, 381, 141))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.icon_lb = QtWidgets.QLabel(self.groupBox)
        self.icon_lb.setGeometry(QtCore.QRect(10, 30, 101, 91))
        self.icon_lb.setText("")
        self.icon_lb.setObjectName("icon_lb")
        icon = QtGui.QPixmap(source_image)
        self.icon_lb.setPixmap(icon.scaled(self.icon_lb.size(), QtCore.Qt.KeepAspectRatio))

        self.text_lb = QtWidgets.QLabel(self.groupBox)
        self.text_lb.setGeometry(QtCore.QRect(140, 30, 221, 91))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.text_lb.setFont(font)
        self.text_lb.setText("")
        self.text_lb.setObjectName("text_lb")
        self.text_lb.setText(message)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
