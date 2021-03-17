from PyQt5 import QtCore, QtGui, QtWidgets
from main_process import *


class MyThread(QtCore.QThread):
    change_value_progress = QtCore.pyqtSignal(int)
    update_console_list = QtCore.pyqtSignal(list)
    data_graph = QtCore.pyqtSignal(list, list)

    def run(self):
        main_process = MainProcess(file_name="Inputs/example_video/1_1.mp4")
        main_process.set_blue_HSV(self.get_blue_HSV())
        main_process.set_laser_HSV(self.get_laser_HSV())

        for i in range(1, main_process.get_index() + 1):
            main_process.process_image(i)
            cnt = int(i*100/main_process.get_index())
            self.change_value_progress.emit(cnt)
            self.update_console_list.emit([i, main_process.distance_x])
            self.data_graph.emit(main_process.ind_array, main_process.dis_array)

    def set_blue_HSV(self, blue_HSV):
        self.blue_HSV = blue_HSV

    def get_blue_HSV(self):
        return self.blue_HSV

    def set_laser_HSV(self, laser_HSV):
        self.laser_HSV = laser_HSV

    def get_laser_HSV(self):
        return self.laser_HSV