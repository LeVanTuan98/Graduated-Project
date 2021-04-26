from main_process import *
from calib_function import *
import os


dir_path = 'Inputs/LAB/'
dir_list = []
for root, dirs, files in os.walk(dir_path):

    # removes hidden files and dirs
    files = [f for f in files if not f[0] == '.']
    dirs = [d for d in dirs if not d[0] == '.']

    if files:
        tag = os.path.relpath(root, dir_path)

        for file in files:
            tag_parent = os.path.dirname(tag)

            sub_folder = os.path.basename(tag)

            # print("File:", file, "belongs in", tag_parent, sub_folder if sub_folder else "")
            file_path = "{}/{}/{}/".format(dir_path, tag_parent, sub_folder if sub_folder else "")
            dir_list.append(file_path)
            # print(file_path)

print(dir_list)
video_list = ['X.mp4', 'Y.mp4']
time = 0
blue_HSV_X = (0, 0, 0)
laser_HSV_X = (0, 0, 0)
blue_HSV_Y = (0, 0, 0)
laser_HSV_Y = (0, 0, 0)
direction = -1
for folder in dir_list:
    time += 1
    for file in video_list:
        file_name = folder + file
        print(file_name)
        video_process = MainProcess(file_name)
        video_process.check_folder()
        # print(video_process.get_folder_address())

        if video_process.get_index() == 0:
            frame_folder, image_folder, excel_folder = video_process.get_folder_address()
            cap = cv2.VideoCapture(video_process.video_address)
            while True:
                # Read a new frame
                ok, frame = cap.read()
                if not ok:
                    # Neu khong doc duoc tiep thi out
                    break
                else:
                    video_process.index += 1
                    frame_address = frame_folder + '/Frame' + str('{0:04}'.format(video_process.index)) + '.jpg'
                    # print(frame_address)
                    cv2.imwrite(frame_address, frame)
        if file == 'X.mp4':
            direction = 0
        elif file == 'Y.mp4':
            direction = 1

        # if time == 1:
        #     calib_process = Calibrate(video_process.get_frame(50))
        #     calib_process.run()
        #     if file == 'X.mp4':
        #         blue_HSV_X = calib_process.get_blue_HSV()
        #         laser_HSV_X = calib_process.get_laser_HSV()
        #         direction = 0
        #     elif file == 'Y.mp4':
        #         blue_HSV_Y = calib_process.get_blue_HSV()
        #         laser_HSV_Y = calib_process.get_laser_HSV()
        #         direction = 1

        # if file == 'X.mp4':
        #     video_process.set_blue_HSV(blue_HSV_X)
        #     video_process.set_laser_HSV(laser_HSV_X)
        #
        # elif file == 'Y.mp4':
        #     video_process.set_blue_HSV(blue_HSV_Y)
        #     video_process.set_laser_HSV(laser_HSV_Y)

        for i in range(1, video_process.get_index() + 1):
            video_process.process_image(i)
        video_process.save_excel_file(direction)










