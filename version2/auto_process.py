from main_process import *
from calib_function import *
import os


dir_path = 'Inputs/'
dir_list = []
for root, dirs, files in os.walk(dir_path):

    # removes hidden files and dirs
    files = [f for f in files if not f[0] == '.']
    dirs = [d for d in dirs if not d[0] == '.']

    if files:
        tag = os.path.relpath(root, dir_path)

        tag_parent = os.path.dirname(tag)

        sub_folder = os.path.basename(tag)

        # print("File:", file, "belongs in", tag_parent, sub_folder if sub_folder else "")
        file_path = "{}/{}/{}".format(dir_path, tag_parent if tag_parent else "", sub_folder if sub_folder else "")
        for file_name in glob.glob(file_path + '/*.mp4'):
            dir_list.append(file_name)
            # print(file_path)

print(dir_list)
blue_HSV_X = (0, 0, 0)
laser_HSV_X = (0, 0, 0)
blue_HSV_Y = (0, 0, 0)
laser_HSV_Y = (0, 0, 0)
direction = -1
for file_name in dir_list:
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


    for i in range(1, video_process.get_index() + 1):
        video_process.process_image(i)
    video_process.save_excel_file()










