import cv2


class Calibrate():
    def __init__(self, image):
        self.image = image
        self.is_laser = 0
        self.blue_HSV = (0, 0, 0)
        self.laser_HSV = (0, 0, 0)
        self.calib_image = cv2.resize(self.image, (720, 480))
        self.HSV_image = cv2.cvtColor(self.calib_image, cv2.COLOR_BGR2HSV)
        self.fill_text_image = self.calib_image.copy()

    def run(self):
        print('CHON 2 THONG SO MAU SAC TREN HINH')
        print("Press c to continue")
        print("Press r to reset")
        print('\r\nChon thong so cho vung mau xanh')


        cv2.namedWindow('CHON 2 THONG SO MAU SAC TREN HINH')
        cv2.setMouseCallback('CHON 2 THONG SO MAU SAC TREN HINH', self.click_HSV)
        cv2.imshow('CHON 2 THONG SO MAU SAC TREN HINH', self.calib_image)

        while True:
            key = cv2.waitKey(1) & 0xFF
            # if the 'r' key is pressed, reset the loop
            if key == ord("r"):
                print('\r\nChon thong so cho vung mau xanh')
                self.is_laser = 0
                self.fill_text_image = self.calib_image.copy()
            # if the 'c' key is pressed, break out the loop
            elif key == ord("c"):
                self.is_laser += 1
                if self.is_laser == 1:
                    print('Chon thong so cho vung laser')
            elif (key == ord('q')) or (self.is_laser > 1):
                print('Hoan tat viec chon 2 thong so')
                cv2.destroyWindow('CHON 2 THONG SO MAU SAC TREN HINH')
                break
        cv2.destroyAllWindows()



    def click_HSV(self, event, x, y, flags, param):
        font = cv2.FONT_HERSHEY_COMPLEX
        if event == cv2.EVENT_LBUTTONDOWN:  # checks mouse left button down condition
            hue = self.HSV_image[y, x, 0]
            sat = self.HSV_image[y, x, 1]
            val = self.HSV_image[y, x, 2]

            cv2.putText(self.fill_text_image, "({H}, {S}, {V})".format(H=hue, S=sat, V=val), (x, y), font, 0.5, (0, 255,255))
            cv2.imshow('CHON 2 THONG SO MAU SAC TREN HINH', self.fill_text_image)

            if self.is_laser == 0:
                print('Blue color: ({H}, {S}, {V})'.format(H=hue, S=sat, V=val))
                self.blue_HSV = [hue, sat, val]
            elif self.is_laser == 1:
                print('Laser color: ({H}, {S}, {V})'.format(H=hue, S=sat, V=val))
                self.laser_HSV = [hue, sat, val]


    def get_blue_HSV(self):
        return self.blue_HSV

    def get_laser_HSV(self):
        return self.laser_HSV






