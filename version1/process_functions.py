import numpy as np
import cv2
import os
import imutils
import matplotlib.pyplot as plt
import shutil
import glob
import xlsxwriter



class Process:

    def __init__(self):
        # HSV: Hue - Saturate - Value
        self.blue_lower = (80, 89, 44) #(80, 89, 44)
        self.blue_upper = (175, 230, 190) #(140, 229, 184)

        self.laser_lower = (140, 0, 245)
        self.laser_upper = (255, 255, 255)

        self.threshold = 0
        self.error_list = []

    def set_threshold(self, threshold):
        self.threshold = threshold

    def set_blue_HSV(self, blue_HSV=(0, 0, 0)):
        if blue_HSV[0] != 0 or blue_HSV[1] != 0 or blue_HSV[2] != 0:
            # HSV: Hue - Saturate - Value
            self.blue_lower = (int(blue_HSV[0] - 30), int(blue_HSV[1] - 70), int(blue_HSV[2] - 70))
            self.blue_upper = (int(blue_HSV[0] + 30), int(blue_HSV[1] + 70), int(blue_HSV[2] + 70))
        else:
            pass

    def get_blue_HSV(self):
        return [self.blue_lower, self.blue_upper]

    def set_laser_HSV(self, laser_HSV=(0, 0, 0)):
        if laser_HSV[0] != 0 or laser_HSV[1] != 0 or laser_HSV[2] != 0:
            # HSV: Hue - Saturate - Value
            self.laser_lower = (int(laser_HSV[0] - 10), int(laser_HSV[1] - 10), int(laser_HSV[2] - 10))
            self.laser_upper = (255, 255, 255)
        else:
            pass

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

                    maskLaser = cv2.inRange(hsvLaserZone, self.laser_lower,
                                            self.laser_upper)  # Ảnh này show ra laser nếu có

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
            # self.error_list.append()
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
                # print("-----------", "Threshold for grid: ", thresholds[i], "------------")
                # print(np.sum(histogram[0, :thresholds[i]]))
                return thresholds[i]

    def detect_dot_of_line(self, mask):
        size_image = np.shape(mask)

        # findcontours
        cnts = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[-2]

        # filter by area
        number_dot_per_line = 15
        S_min = 5
        S_max = 300
        x = []
        y = []

        # Tim tam cua cac nut luoi dua vao dieu kien dien tich [S_min, S_max]
        for cnt in cnts:
            if S_min < cv2.contourArea(cnt) < S_max:
                # calculate moments of binary image
                M = cv2.moments(cnt)

                # calculate x,y coordinate of center
                grid_x = int(M["m10"] / M["m00"])
                grid_y = int(M["m01"] / M["m00"])

                SD = 10
                if (SD < grid_x < size_image[1] - SD) and (SD < grid_y < size_image[0] - SD):
                    x.append(grid_x)
                    y.append(grid_y)
        x = np.array(x)
        y = round(np.array(y).mean())
        x.sort()
        # print(len(x))
        # print(x)

        while(len(x) != number_dot_per_line):
            if len(x) < number_dot_per_line:
                for i in range(number_dot_per_line - len(x)):
                    diff_x = np.diff(x)
                    diff2_x = np.diff(diff_x)
                    abnormal_value = np.where(abs(diff2_x) > 5)[0]
                    if abnormal_value.size != 0:
                        # max_value = np.amax(diff_x)
                        max_index = np.where(diff_x == np.amax(diff_x))[0][0]
                        mean_value = round(np.delete(diff_x, max_index).mean())
                        x = np.insert(x, max_index + 1, (x[max_index] + mean_value))
                        x.sort()
                        # print(diff_x)
                        # print(x)
                    else:
                        mean_value = round(diff_x.mean())
                        if (size_image[1] - x[-1]) > 50:
                            x = np.insert(x, -1, (x[-1] + mean_value))
                        elif x[0] > 50:
                            x = np.insert(x, 0, mean_value)
                        x.sort()
            else:
                diff_x = np.diff(x)
                diff2_x = np.diff(diff_x)
                abnormal_value = np.where(abs(diff2_x) > 5)[0]
                x = np.delete(x, abnormal_value[0] + 2)
                x.sort()

        y = np.ones_like(x) * y
        return x, y

    def detect_grid_coodinate(self, warped_image):
        image = warped_image.copy()
        size_image = np.shape(image)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # thresholding
        th, threshed_image = cv2.threshold(gray, self.threshold, 255, cv2.THRESH_BINARY_INV)
        upper_line_mask = np.zeros_like(threshed_image)
        lower_line_mask = np.zeros_like(threshed_image)
        # Upper line
        [top, bottom, left, right] = [5, int(size_image[0] * 1/3), 20, int(size_image[1] - 20)]
        upper_line_mask[top:bottom][left:right] = threshed_image[top:bottom][left:right]
        # Lower line
        [top, bottom, left, right] = [int(size_image[0] * 3/5), int(size_image[0] - 10), 20, int(size_image[1] - 20)]
        lower_line_mask[top:bottom][left:right] = threshed_image[top:bottom][left:right]

        # [DEBUG MODE]
        # cv2.imshow("threshed_image", threshed_image)
        # cv2.imshow("upper line mask", upper_line_mask)
        # cv2.imshow("lower line mask", lower_line_mask)
        # cv2.waitKey(0)

        x1, y1 = self.detect_dot_of_line(upper_line_mask)
        x2, y2 = self.detect_dot_of_line(lower_line_mask)

        line1 = []  # toa do cua cac diem hang tren
        line2 = []  # toa do cac diem hang duoi
        ver_coor = []  # toa do cac diem theo truc x
        delta = []  # xac dinh do lech giua x1 va x2
        for i in range(15):
            line1.append([x1[i], y1[i]])
            line2.append([x2[i], y2[i]])
            mean_x = round((x1[i] + x2[i])/2)
            ver_coor.append(mean_x)
            delta.append(x1[i] - x2[i])

        return line1, line2, ver_coor, round(np.mean(delta))

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



