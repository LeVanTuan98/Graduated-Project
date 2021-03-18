from process_functions import *


class MainProcess(Process):

    def __init__(self, file_name=""):
        super().__init__()
        self.index = 0
        self.dis_array = []
        self.ind_array = []
        self.video_address = file_name
        self.final_width = 620
        self.final_height = 180
        self.pre_line1 = 0
        self.pre_line2 = 0
        self.pre_ver_coor = 0
        self.distance_x = 0

    def get_folder_address(self):
        path_video = ""
        is_path = False
        path = self.video_address.split('.')[0]
        path = path.split('/')
        for i in range(len(path) - 1):
            if path[i] == 'Inputs':
                is_path = True
                continue
            if is_path:
                path_video += path[i] + '/'
        path_video += path[-1]
        print("Path_video_in_project:", path_video)

        frame_folder = 'Outputs/' + path_video + '/frameFolder'
        image_folder = 'Outputs/' + path_video + '/imageFolder'
        excel_folder = 'Outputs/' + path_video + '/excelFolder'
        return frame_folder, image_folder, excel_folder

    def check_folder(self):
        frame_folder, image_folder, excel_folder = self.get_folder_address()

        if not os.path.exists(frame_folder):
            os.makedirs(frame_folder)
        if not os.path.exists(excel_folder):
            os.makedirs(excel_folder)
        if os.path.exists(image_folder):
            shutil.rmtree(image_folder)
        os.makedirs(image_folder)

    def get_save_address(self):
        _, _, excel_folder = self.get_folder_address()
        save_address = excel_folder + '/time-distance.xlsx'
        return save_address

    def get_index(self):
        frame_folder, _, _ = self.get_folder_address()
        if self.index == 0:
            path, dirs, files = next(os.walk(frame_folder))
            return len(files)
        else:
            return self.index

    def get_image_address(self, ind_image):
        _, img_folder, _ = self.get_folder_address()
        img_address = []
        for filename in glob.glob(img_folder + '/*.jpg'):
            img_address.append(filename)
            # print(filename)
        return img_address[ind_image]

    def get_image(self, ind_image):
        frame_folder, _, _ = self.get_folder_address()
        frame_address = frame_folder + '/Frame' + str('{0:04}'.format(ind_image) + '.jpg')
        return cv2.imread(frame_address)

    def process_image(self, ind_image):
        # STEP 1: Load image
        original_image = self.get_image(ind_image)
        # cv2.imshow("Original image", cv2.resize(src=original_image, dsize=(500, 200)))

        # STEP 2: Detect WHITE frame
        white_frame = super().detect_white_frame(original_image)
        if white_frame.shape == original_image.shape:
            print("[ERROR] in STEP 2")
            return
        # cv2.imshow("Detected white frame", white_frame)
        # cv2.imwrite("detect.jpg", white_frame)

        # STEP 3: Determine the coordinate of the Grid
        threshold_grid = super().determine_threshold_for_grid(white_frame)
        super().set_threshold(threshold_grid)

        line1, line2, ver_coor, translation = super().detect_grid_coodinate(white_frame)

        if np.size(ver_coor) != 15:
            threshold_grid = super().determine_threshold_for_grid(white_frame)
            super().set_threshold(threshold_grid)

            # STEP 4: Determine the coordinate of the Grid - Lap lai buoc 4
            line1, line2, ver_coor, translation = super().detect_grid_coodinate(white_frame)

            if np.size(ver_coor) != 15:
                line1 = self.pre_line1
                line2 = self.pre_line2
                ver_coor = self.pre_ver_coor
                if np.size(self.pre_ver_coor) != 15:
                    print("[ERROR] in STEP 3")
                    return

        self.pre_line1 = line1
        self.pre_line2 = line2
        self.pre_ver_coor = ver_coor

        # STEP 4: Find center point
        cX, cY = super().find_center_point(white_frame)
        if cX == -1:
            print("[ERROR] in STEP 4")
            return

        # STEP 5: Calculate the real coordinate of the laser pointer
        self.distance_x = super().calculate_real_coordinate_of_laser_pointer(cX, cY, ver_coor)
        print("Khoang cach: " + str(self.distance_x))

        _, image_folder, _ = self.get_folder_address()
        image_address = image_folder + '/Image' + str('{0:04}-{distance}'.format(ind_image, distance=self.distance_x)) + '.jpg'
        print(image_address)

        # STEP 6: Draw and Save image
        final_image = super().shift_image(white_frame, translation)
        font = cv2.FONT_HERSHEY_COMPLEX
        for j in range(15):
            cv2.line(final_image, (line1[j][0] + translation, line1[j][1]), (line2[j][0], line2[j][1]),
                     (0, 0, 0), 1)

        cv2.circle(final_image, (cX, cY), 5, (0, 0, 255), 1, cv2.LINE_AA)
        cv2.line(final_image, (cX, cY), (ver_coor[0], cY), (0, 0, 255), 1)
        cv2.putText(final_image, str(self.distance_x) + 'cm', (int(cX / 2), cY - 10), font, 0.5, (255, 0, 0))
        final_img_size = np.shape(final_image)

        final_image = cv2.resize(src=final_image[:, abs(translation):final_img_size[1] - abs(translation), :],
                                 dsize=(self.final_width, self.final_height))
        cv2.imwrite(image_address, final_image)

        # STEP 7: Calculate the distance change
        self.dis_array.append(self.distance_x)
        self.ind_array.append(ind_image)

    def save_excel_file(self):
        workbook = xlsxwriter.Workbook(self.get_save_address())
        worksheet = workbook.add_worksheet('result')
        col = 0
        worksheet.write_row(0, col, ['Frame', 'Distance(cm)'])
        for i in self.ind_array:
            worksheet.write_row(i, col, [i, self.dis_array[i - 1]])
        workbook.close()
