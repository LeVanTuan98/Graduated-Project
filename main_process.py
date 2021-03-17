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
        self.path_video = self.video_address.split('.')[0]
        self.frameFolder_address = 'Outputs/' + self.path_video + '/frameFolder'
        self.imageFolder_address = 'Outputs/' + self.path_video + '/imageFolder'

    def check_folder(self):
        if not os.path.exists(self.frameFolder_address):
            os.makedirs(self.frameFolder_address)
        if os.path.exists(self.imageFolder_address):
            shutil.rmtree(self.imageFolder_address)
        os.makedirs(self.imageFolder_address)

    def get_index(self):
        if self.index == 0:
            path, dirs, files = next(os.walk(self.frameFolder_address))
            return len(files)
        else:
            return self.index

    def get_image(self, ind_image):
        frame_address = 'Outputs/' + self.path_video + '/frameFolder' + '/Frame' + str(
            '{0:04}'.format(ind_image) + '.jpg')
        return cv2.imread(frame_address)

    def extract_frame(self):
        cap = cv2.VideoCapture(self.video_address)
        while True:
            # Read a new frame
            ok, frame = cap.read()
            if not ok:
                # Neu khong doc duoc tiep thi out
                break
            else:
                self.index += 1
                frame_address = 'Outputs/' + self.path_video + '/frameFolder' + '/Frame' + str('{0:04}'.format(
                    self.index)) + '.jpg'
                # print(frame_address)
                cv2.imwrite(frame_address, frame)

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

        image_address = 'Outputs/' + self.path_video + '/imageFolder' + '/Image' + str('{0:04}-{distance}'.format(
            ind_image,
            distance=self.distance_x
        )) + '.jpg'
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