from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QImage


from PyQt5.QtWidgets import (
    QApplication,
    QDialog,
    QDialogButtonBox,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QFileDialog)


from main_process import *
from custome_dialog import *


class MainFrame(QtWidgets.QLabel):

    def __init__(self, object):
        super().__init__(object)
        self.image = None
        self.ratio = (0, 0)
        self.blue_HSV = (0, 0, 0)
        self.laser_HSV = (0, 0, 0)
        self.is_laser = 0
        self.font = cv2.FONT_HERSHEY_COMPLEX

    clicked = QtCore.pyqtSignal()

    def mousePressEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            x = event.x()
            y = event.y()
            self.clicked.emit()
            scaled_image = cv2.resize(self.image, self.ratio)
            y0 = int((self.size().height() - scaled_image.shape[0]) / 2)
            x0 = int((self.size().width() - scaled_image.shape[1]) / 2)
            x -= x0
            y -= y0
            if 0 <= x <= scaled_image.shape[1] and 0 <= y <= scaled_image.shape[0]:
                calib_image = Process()
                HSV_image = calib_image.convert_RGB_to_HSV(scaled_image)
                hue = HSV_image[y, x, 0]
                sat = HSV_image[y, x, 1]
                val = HSV_image[y, x, 2]
                if self.is_laser == 0:
                    dlg = CustomDialog(
                        message="1. Chon thong so cho vung mau xanh \r\nBlue color: ({H}, {S}, {V})".format(H=hue,
                                                                                                            S=sat,
                                                                                                            V=val))
                    if dlg.exec_():
                        self.blue_HSV = (hue, sat, val)
                        self.is_laser += 1
                        cv2.putText(scaled_image, "({H}, {S}, {V})".format(H=hue, S=sat, V=val), (x, y), self.font, 0.5,
                                    (0, 255, 255))
                        # print('Blue color: ({H}, {S}, {V})'.format(H=hue, S=sat, V=val))
                        self.show_main_frame(scaled_image)
                    else:
                        self.is_laser = 0
                elif self.is_laser == 1:
                    dlg = CustomDialog(
                        message="2. Chon thong so cho vung laser \r\nLaser color: ({H}, {S}, {V})".format(H=hue,
                                                                                                          S=sat,
                                                                                                          V=val))
                    if dlg.exec_():
                        self.laser_HSV = (hue, sat, val)
                        self.is_laser += 1
                        cv2.putText(scaled_image, "({H}, {S}, {V})".format(H=hue, S=sat, V=val), (x, y), self.font, 0.5,
                                    (0, 255, 255))
                        # print('Laser color: ({H}, {S}, {V})'.format(H=hue, S=sat, V=val))
                        self.show_main_frame(scaled_image)
                    else:
                        self.is_laser = 1
            else:
                dlg = CustomDialog(type='alert', message="CLICK VAO DUNG KHUNG HINH")
                dlg.exec_()
                return

    def show_main_frame(self, image):
        self.image = image
        q_img = self.convert_cvImg_to_qImg(image)
        frame = QtGui.QPixmap(q_img).scaled(self.size(), QtCore.Qt.KeepAspectRatio)
        self.ratio = (frame.size().width(), frame.size().height())
        self.setPixmap(frame)

    def convert_cvImg_to_qImg(self, cv_img):
        height, width, channel = cv_img.shape
        bytes_per_line = 3 * width
        q_img = QImage(cv_img.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
        return q_img
