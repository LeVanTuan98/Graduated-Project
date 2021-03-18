from PyQt5 import QtCore, QtGui, QtWidgets
from main_process import *


class RunThread(QtCore.QThread):
    change_value_progress = QtCore.pyqtSignal(int)
    update_console_list = QtCore.pyqtSignal(list)
    data_graph = QtCore.pyqtSignal(list, list)
    total_image = QtCore.pyqtSignal(int)
    run_progess_finished = QtCore.pyqtSignal(bool)

    def run(self):
        main_process = MainProcess(file_name=self.file_path)
        main_process.set_blue_HSV(self.get_blue_HSV())
        main_process.set_laser_HSV(self.get_laser_HSV())

        for i in range(1, main_process.get_index() + 1):
            main_process.process_image(i)
            cnt = int(i*100/main_process.get_index())
            self.change_value_progress.emit(cnt)
            self.update_console_list.emit([i, main_process.distance_x])
            self.data_graph.emit(main_process.ind_array, main_process.dis_array)
        main_process.save_excel_file()
        self.total_image.emit(main_process.get_index())
        self.run_progess_finished.emit(True)

    def set_blue_HSV(self, blue_HSV):
        self.blue_HSV = blue_HSV

    def get_blue_HSV(self):
        return self.blue_HSV

    def set_laser_HSV(self, laser_HSV):
        self.laser_HSV = laser_HSV

    def get_laser_HSV(self):
        return self.laser_HSV

    def set_file_path(self, file_path):
        self.file_path = file_path


class CalibThread(QtCore.QThread):
    change_value_progress = QtCore.pyqtSignal(int)
    calib_progess_finished = QtCore.pyqtSignal(bool)

    def run(self):
        main_process = MainProcess(file_name=self.file_path)
        main_process.check_folder()
        if main_process.get_index() == 0:
            frame_folder, _, _ = main_process.get_folder_address()
            cap = cv2.VideoCapture(main_process.video_address)
            while True:
                # Read a new frame
                ok, frame = cap.read()
                if not ok:
                    # Neu khong doc duoc tiep thi out
                    break
                else:
                    main_process.index += 1
                    frame_address = frame_folder + '/Frame' + str('{0:04}'.format(main_process.index)) + '.jpg'
                    # print(frame_address)
                    cv2.imwrite(frame_address, frame)
                    cnt = int(main_process.index * 100 / 1000) #Notices 1000: phụ thuộc vào chiều dài video
                    self.change_value_progress.emit(cnt)

            self.calib_progess_finished.emit(True)
        else:
            self.change_value_progress.emit(100)
            self.calib_progess_finished.emit(True)

    def set_file_path(self, file_path):
        self.file_path = file_path