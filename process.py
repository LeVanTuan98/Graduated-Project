import numpy as np
import cv2
import os
import imutils
import matplotlib.pyplot as plt

class Process:

    def __init__(self):
        # HSV: Hue - Saturate - Value
        self.blue_lower = (80, 89, 44)
        self.blue_upper = (140, 229, 184)

        self.laser_lower = (140, 0, 245)
        self.laser_upper = (255, 255, 255)

        self.threshold = 0

    def set_threshold(self, threshold):
        self.threshold = threshold

    def set_blue_HSV(self, blue_HSV=(0, 0, 0)):
        # HSV: Hue - Saturate - Value
        self.blue_lower = (blue_HSV[0] - 30, blue_HSV[1] - 70, blue_HSV[2] - 70)
        self.blue_upper = (blue_HSV[0] + 30, blue_HSV[1] + 70, blue_HSV[2] + 70)

    def set_laser_HSV(self,laser_HSV=(0, 0, 0)):
        # HSV: Hue - Saturate - Value
        self.laser_lower = (laser_HSV[0] - 10, laser_HSV[1] - 10, laser_HSV[2] - 10)
        self.laser_upper = (255, 255, 255)

    def convert_RGB_to_HSV(self, original_image):
        return cv2.cvtColor(original_image.copy(), cv2.COLOR_BGR2HSV)

    def order_points(self, pts):
        # initialzie a list of coordinates that will be ordered
        # such that the first entry in the list is the top-left,
        # the second entry is the top-right, the third is the
        # bottom-right, and the fourth is the bottom-left
        rect = np.zeros((4, 2), dtype="float32")
        # the top-left point will have the smallest sum, whereas
        # the bottom-right point will have the largest sum
        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]
        # now, compute the difference between the points, the
        # top-right point will have the smallest difference,
        # whereas the bottom-left will have the largest difference
        diff = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]
        # return the ordered coordinates
        return rect

    def four_point_transform(self, image, pts):
        # obtain a consistent order of the points and unpack them
        # individually
        rect = self.order_points(pts)
        (tl, tr, br, bl) = rect
        # compute the width of the new image, which will be the
        # maximum distance between bottom-right and bottom-left
        # x-coordiates or the top-right and top-left x-coordinates
        widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
        widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
        maxWidth = max(int(widthA), int(widthB))

        minX = min(tl[0], bl[0])
        maxX = max(tr[0], br[0])

        # compute the height of the new image, which will be the
        # maximum distance between the top-right and bottom-right
        # y-coordinates or the top-left and bottom-left y-coordinates
        heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
        heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
        maxHeight = max(int(heightA), int(heightB))

        minY = min(tl[1], tr[1])
        maxY = max(bl[1], br[1])
        # now that we have the dimensions of the new image, construct
        # the set of destination points to obtain a "birds eye view",
        # (i.e. top-down view) of the image, again specifying points
        # in the top-left, top-right, bottom-right, and bottom-left
        # order
        dst = np.array([
            [0, 0],
            [maxWidth - 1, 0],
            [maxWidth - 1, maxHeight - 1],
            [0, maxHeight - 1]], dtype="float32")
        # compute the perspective transform matrix and then apply it
        M = cv2.getPerspectiveTransform(rect, dst)
        warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
        # return the warped image
        return warped, minX, maxX, minY, maxY

    def detect_white_frame(self, original_image):
        image = original_image.copy()

        # convert the image to grayscale, blur it, and find edges
        # in the image
        blurred = cv2.GaussianBlur(image, (5, 5), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

        maskBlue = cv2.inRange(hsv, self.blue_lower, self.blue_upper)

        maskBlue = cv2.erode(maskBlue, None, iterations=2)
        maskBlue = cv2.dilate(maskBlue, None, iterations=2)

        # show the original image and the edge detected image
        ## STEP 1: Color Detection - BLUE

        # 1.1 Finding Contours
        # find the contours in the edged image, keeping only the
        # largest ones, and initialize the screen contour
        cntsBlue = cv2.findContours(maskBlue.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
        cntsBlue = imutils.grab_contours(cntsBlue)
        cntsBlue = sorted(cntsBlue, key=cv2.contourArea, reverse=True)[:4]

        # [DEBUG MODE]
        # cv2.imwrite("Warped blue image.jpg", maskBlue)
        # print(np.shape(cntsBlue))
        # cv2.imshow("Warped blue image", cv2.resize(maskBlue, (500, 250)))
        # cv2.waitKey(0)

        screenCntWhite = np.zeros_like(original_image)  # Khởi tạo vùng màu đen không có gì
        try:
            # loop over the contours
            for i in range(np.size(cntsBlue)):
                peri = cv2.arcLength(cntsBlue[i], True)
                approx_blue = cv2.approxPolyDP(cntsBlue[i], 0.02 * peri, True)

                # Đầu tiên, tìm vùng bao hình chữ nhật màu xanh có chứa laser,
                # Nếu có, thì tiếp tục dịch vào để tìm viền của khung màu trắng
                if len(approx_blue) == 4:
                    maskBlue = np.zeros_like(original_image)
                    cv2.drawContours(maskBlue, [approx_blue], 0, (255, 255, 255), -1)  # Draw filled contour in mask

                    blueZone = np.zeros_like(original_image)  # Extract out the object and place into output image
                    blueZone[maskBlue == 255] = original_image[maskBlue == 255]

                    hsvLaserZone = cv2.cvtColor(blueZone.copy(), cv2.COLOR_BGR2HSV)

                    maskLaser = cv2.inRange(hsvLaserZone, self.laser_lower, self.laser_upper)  # Ảnh này show ra laser nếu có

                    laserZone = np.zeros_like(original_image)  # Extract out the object and place into output image
                    laserZone[maskLaser == 255] = original_image[maskLaser == 255]

                    # # [DEBUG MODE]
                    # cv2.imshow('The photo contains only laser dot', cv2.resize(laserZone, (500, 200)))
                    # cv2.imshow('Laser Mask ', cv2.resize(maskLaser, (500, 200)))
                    # cv2.imwrite("laser zone.jpg", laserZone)
                    # cv2.imwrite("laser mask.jpg", maskLaser)

                    # cv2.imshow('The photo contains blue zone', cv2.resize(blueZone, (500, 250)))
                    # cv2.imshow('Blue Mask ', cv2.resize(maskBlue, (500, 200)))
                    # cv2.imwrite("Blue Mask.jpg", blueZone)
                    # cv2.waitKey(0)

                    # calculate moments of binary image
                    M = cv2.moments(maskLaser)

                    try:
                        # calculate x,y coordinate of center
                        cXTemp = int(M["m10"] / M["m00"])
                        cYTemp = int(M["m01"] / M["m00"])

                    except:
                        print("[LOG] Khong tim thay laser.")
                        continue
                    # Nếu thỏa mãn vùng màu xanh có chứa Laser thì tiếp tục để tìm vùng trắng bên trong
                    # loop over the contours
                    for j in range(i + 1, np.size(cntsBlue)):
                        # approximate the contour
                        peri = cv2.arcLength(cntsBlue[j], True)
                        approx_white = cv2.approxPolyDP(cntsBlue[j], 0.02 * peri, True)

                        maskWhite = np.zeros_like(original_image)
                        cv2.drawContours(maskWhite, [approx_white], 0, (255, 255, 255),
                                         -1)  # Draw filled contour in mask

                        whiteZone = np.zeros_like(original_image)  # Extract out the object and place into output image
                        whiteZone[maskWhite == 255] = original_image[maskWhite == 255]

                        # # [DEBUG MODE]
                        # cv2.imshow('The photo contains white zone', cv2.resize(whiteZone, (500, 250)))
                        # cv2.imshow('White Mask ', cv2.resize(maskBlue, (500, 200)))
                        # cv2.waitKey(0)

                        blueArea = cv2.contourArea(cntsBlue[i])
                        whiteArea = cv2.contourArea(cntsBlue[j])
                        # print(blueArea)
                        # print(whiteArea)
                        # print(i, j)

                        # if our approximated contour has four points, then we
                        # can assume that we have found our screen
                        if len(approx_white) == 4:
                            _, minX, maxX, minY, maxY = self.four_point_transform(whiteZone, approx_white.reshape(4, 2))
                            if minX < cXTemp < maxX and minY < cYTemp < maxY and (0.5 < (whiteArea / blueArea) < 1):
                                screenCntWhite = approx_white

                                # [DEBUG MODE]
                                # cv2.imshow('Detected white zone', screenCntWhite)

                                finalWhiteImage, _, _, _, _ = self.four_point_transform(original_image,
                                                                                   screenCntWhite.reshape(4, 2))
                                # cv2.imshow('Mask_wapred.jpg', finalWhiteImage)
                                # cv2.imwrite('Mask_wapred.jpg', finalWhiteImage)
                                return finalWhiteImage
                            else:
                                continue
        except:
            print("[WARNING] Khong co vung trang thoa man")
        return screenCntWhite

    def find_center_point(self, warped_image):
        ## Find centre of laser poiter (x, y)
        frame = warped_image.copy()
        hsvWar = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        maskWar = cv2.inRange(hsvWar, self.laser_lower, self.laser_upper)

        # maskWar = cv2.erode(maskWar, None, iterations=1)
        # maskWar = cv2.dilate(maskWar, None, iterations=1)  # Đang là ảnh Gray với 2 mức xám 0 và 255

        # calculate moments of binary image
        M = cv2.moments(maskWar)
        try:
            # calculate x,y coordinate of center
            x = int(M["m10"] / M["m00"])
            y = int(M["m01"] / M["m00"])
        except:
            print("[ERROR] Tach Frame da loi")
            return -1, -1

        # cv2.circle(warped_image, (x, y), 5, (0, 0, 255), 1, cv2.LINE_AA)
        # cv2.imshow("laser position", warped_image)

        # Improve the algorithm finding the centre laser
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # color -> gray
        blurred = cv2.GaussianBlur(gray, (3, 3), 0)
        thresh = cv2.threshold(blurred, 240, 255, cv2.THRESH_BINARY_INV)[1]
        canny = cv2.Canny(thresh, 50, 255, 1)
        # cv2.imshow('canny', canny)

        delta = 30
        if (x < delta) | (y < delta):
            delta = 15

        mask_laser = canny[y - delta: y + delta, x - delta: x + delta]
        # Focusing on [top right bottom left] of red region
        [top, bottom, left, right] = self.FindTRBL(mask_laser)
        if (top == 0) & (bottom == 0) & (left == 0) & (right == 0):
            return x, y
        cX = x + int((right + left) / 2) - delta
        cY = y + int((top + bottom) / 2) - delta
        return cX, cY

    def FindTRBL(self, values):
        # Input: Ma tran can tim T - R - B - L
        # Output: Gia tri cua Tmost - Rmost - Bmost - Lmost
        leftmost = 0
        rightmost = 0
        topmost = 0
        bottommost = 0
        temp = 0
        for i in range(np.size(values, 1)):
            col = values[:, i]
            if np.sum(col) != 0.0:
                rightmost = i
                if temp == 0:
                    leftmost = i
                    temp = 1
        for j in range(np.size(values, 0)):
            row = values[j, :]
            if np.sum(row) != 0.0:
                bottommost = j
                if temp == 1:
                    topmost = j
                    temp = 2
        return [topmost, bottommost, leftmost, rightmost]

    def determine_threshold_for_grid(self, warped_image):
        # # Tìm mức ngưỡng phù hợp dựa vào histogram
        image = warped_image.copy()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # cv2.imshow("gray", gray)

        gray = gray[10:np.size(gray, 0) - 10, 10:np.size(gray, 1) - 10]
        # Tìm mức ngưỡng phù hợp dựa vào histogram
        histogram = cv2.calcHist([gray], [0], None, [256], [0, 256])
        plt.plot(histogram, color='k')
        histogram = np.reshape(histogram, (1, 256))

        diff_hist = np.diff(histogram)
        thresholds = []
        for i in range(np.size(diff_hist) - 1):
            if np.sign(diff_hist[0, i]) != np.sign(diff_hist[0, i + 1]):
                if histogram[0, i + 1] > 1500:
                    break
                # print(i + 1, ": ", histogram[0, i + 1])
                # plt.plot(i + 1, histogram[0, i + 1], color='green', linestyle='dashed', linewidth=1,
                #          marker='o', markerfacecolor='red', markersize=5)
                thresholds.append(i + 1)
        # plt.show()
        # print(np.sum(histogram[0, :thresholds[-1]]))
        for i in range(np.size(thresholds) - 1, 0, -1):
            if np.sum(histogram[0, :thresholds[i]]) < 8000:
                print("-----------", "Threshold for grid: ", thresholds[i], "------------")
                # print(np.sum(histogram[0, :thresholds[i]]))
                return thresholds[i]

    def detect_grid_coodinate(self, warped_image):
        image = warped_image.copy()
        size_image = np.shape(image)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # thresholding
        th, threshed = cv2.threshold(gray, self.threshold, 255, cv2.THRESH_BINARY_INV)
        # [DEBUG MODE]
        # cv2.imshow("thresh", threshed)
        # # cv2.imwrite("thresh.jpg", threshed)
        # cv2.waitKey(0)

        # findcontours
        cnts = cv2.findContours(threshed, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[-2]
        # filter by area
        number_dot_per_line = 15
        S_min = 5
        S_max = 300
        xcnts = []
        coor_x = []
        coor_y = []
        # Tim tam cua cac nut luoi dua vao dieu kien dien tich [S_min, S_max]
        for cnt in cnts:
            if S_min < cv2.contourArea(cnt) < S_max:
                # calculate moments of binary image
                M = cv2.moments(cnt)

                # calculate x,y coordinate of center
                grid_x = int(M["m10"] / M["m00"])
                grid_y = int(M["m01"] / M["m00"])

                # [DEBUG MODE]
                # cv2.circle(image, (grid_x, grid_y), 2, (255, 0, 0), 2, cv2.LINE_AA)
                # cv2.imshow("grid_image", image)
                # cv2.waitKey(0)

                SD = 15
                if (SD < grid_x < size_image[1] - SD) and (SD < grid_y < size_image[0] - SD):
                    xcnts.append(cnt)
                    coor_x.append(grid_x)
                    coor_y.append(grid_y)
                    cv2.circle(image, (grid_x, grid_y), 2, (255, 0, 0), 2, cv2.LINE_AA)
                    # cv2.imshow("grid_image", image)
                    # cv2.waitKey(0)

        if len(xcnts) != number_dot_per_line * 2:
            print('[ERROR] Co %d diem nut!!!' % (len(xcnts)))

        # [DEBUG MODE]
        # cv2.imshow("grid_image", image)
        # cv2.waitKey(0)

        # Sap xep cac nut luoi theo tung cap voi cung toa do x
        delta = []  # xac dinh do lech giua x1 va x2
        try:
            line1 = []  # toa do cua cac diem hang tren
            line2 = []  # toa do cac diem hang duoi
            ver_coor = []  # toa do cac diem theo truc x
            # Sap xep cac nut luoi theo tung cap voi cung toa do x
            while len(coor_x) != 0:

                x1 = coor_x[0]
                y1 = coor_y[0]

                coor_x.pop(0)
                coor_y.pop(0)
                # Kiem tra xem co 2 diem nao co toa do x gan nhau ma khong phai la 1 cap
                if np.size(ver_coor) > 0:
                    x1_temp = abs(ver_coor - np.ones(np.size(ver_coor)) * x1)
                    x1_min = min(x1_temp)
                    if x1_min < 10:
                        continue

                if len(coor_x) == 0:
                    x2 = x1
                    y2 = np.shape(image)[0] - 25 if (y1 < 50) else 20
                else:
                    coor_temp = abs(coor_x - np.ones(np.size(coor_x)) * x1)
                    min_temp = min(coor_temp)
                    if min_temp > 20:
                        x2 = x1
                        y2 = np.shape(image)[0] - 25 if (y1 < 50) else 20
                    else:
                        for j in range(len(coor_temp)):
                            if coor_temp[j] == min_temp:
                                index_x2 = j
                                break
                        x2 = coor_x[index_x2]
                        y2 = coor_y[index_x2]
                xtb = int((x1 + x2) / 2)
                if abs(y1 - y2) > 80:
                    coor_x.pop(index_x2)
                    coor_y.pop(index_x2)
                    if y1 < y2:
                        line1.append([x1, y1])
                        line2.append([x2, y2])
                    else:
                        line2.append([x1, y1])
                        line1.append([x2, y2])
                    ver_coor.append(xtb)
                    delta.append(x1 - x2)
                    # print("-----------")
                    # print(coor_x)
                    # print(coor_y)
                    # print(x1, y1)
                    # print(x2, y2)
                    # cv2.circle(image, (x1, y1), 2, (255, 0, 255), 2, cv2.LINE_AA)
                    # cv2.circle(image, (x2, y2), 2, (255, 0, 255), 2, cv2.LINE_AA)
                    # cv2.imshow("grid_image", image)
                    # cv2.waitKey(0)
            ver_coor.sort()
            # print(round(np.average(delta)))
            return line1, line2, ver_coor, int(round(np.average(delta)))
        except:
            print("[ERROR] Khong the xac dinh dung luoi")
            return 0, 0, 0, 0

    def calculate_real_coordinate_of_laser_pointer(self, cX, cY, ver_coor):
        # Input: x, y: Toa do tam cua diem laser
        #        verCoor: Toa do cua cac truc doc
        # Output: [x_real]: Toa do thuc te cua diem laser theo x

        # Kich thuoc thuc cua khung giay [Dai x Rong]
        # real_size = [13.9, 8.9]
        real_size = [1, 2.5]

        delta_x = np.diff(ver_coor)
        # delta_y = np.diff(honCoor)

        # Tinh khoang cach tu tam den duong dau tien ben trai
        # Neu tam nam giua 2 cot => tinh ty le khoang cach tu tam den cot ben trai gan nhat + so cot o giua
        if (cX < min(ver_coor)):
            print("[WARNING] Vuot ra khoi luoi")
            x_real = 0
        if (cX > max(ver_coor)):
            print("[WARNING] Vuot ra khoi luoi")
            x_real = 14
        else:
            delta = ver_coor - np.ones(np.size(ver_coor)) * cX
            minValue = min(abs(delta))
            for i in range(len(delta) - 1):
                if np.sign(delta[i]) != np.sign(delta[i + 1]):
                    # Tinh khoang cach den i - cot ben trai gan nhat
                    scale_x = real_size[0] / (delta_x[i])
                    x_real = round((cX - ver_coor[i]) * scale_x + i, 2)
                if abs(delta[i]) == minValue:
                    if minValue == 0:
                        x_real = i
                    break
        return x_real

    def shift_image(self, original_image, delta):
        image = original_image.copy()
        # Create translation matrix.
        # If the shift is (x, y) then matrix would be
        # M = [1 0 x]
        #     [0 1 y]
        # Let's shift by (100, 50).
        M = np.float32([[1, 0, delta], [0, 1, 0]])
        # Get a part of image
        image_part = int(np.shape(image)[0] / 2)
        img = image[:image_part, :, :]
        (rows, cols) = img.shape[:2]

        # warpAffine does appropriate shifting given the
        # translation matrix.
        res = cv2.warpAffine(img, M, (cols, rows))
        image[:image_part, :, :] = res
        return image

class MainProcess(Process):

    def __init__(self, file_name=""):
        super().__init__()
        self.index = 0
        self.dis_array = []
        self.video_address = file_name
        self.final_width = 620
        self.final_height = 180
        self.pre_line1 = 0
        self.pre_line2 = 0
        self.pre_ver_coor = 0
        self.distance_x = 0
        self.path_video = self.video_address.split('.')[0]
        if not os.path.exists('Outputs/' + self.path_video + '/frameFolder'):
            os.makedirs('Outputs/' + self.path_video + '/frameFolder')
        if not os.path.exists('Outputs/' + self.path_video + '/imageFolder'):
            os.makedirs('Outputs/' + self.path_video + '/imageFolder')

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
        frame_address = 'Outputs/' + self.path_video + '/frameFolder' + '/Frame' + str('{0:04}'.format(ind_image) + '.jpg')
        # STEP 1: Load image
        original_image = cv2.imread(frame_address)
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
                                                                                                self.index,
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
        self.dis_array.append([ind_image, self.distance_x])















