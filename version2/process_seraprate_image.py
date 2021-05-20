import cv2

from process_functions import *

final_width = 620
final_height = 180
pre_line1 = 0
pre_line2 = 0
pre_ver_coor = 0
distance_x = 0
number_of_frame = 1
rotate_image = False
def sort_func(e):
    return e[0]

image_name = '60_2.jpg'
input_image_file = "Inputs/LAB/May18/TEST/" + image_name

# cap = cv2.VideoCapture(input_image_file)
i = 0.0
dis_array = []


process_image = Process()

# STEP 1: Load image
original_image = cv2.imread(input_image_file)
if rotate_image:
    original_image = cv2.rotate(original_image, cv2.ROTATE_90_CLOCKWISE)
# cv2.imshow("Original image", cv2.resize(src=original_image, dsize=(500, 200)))


# STEP 2: Detect WHITE frame
set_of_white_frame = process_image.detect_white_frame(original_image)
print(np.shape(set_of_white_frame))
if np.shape(set_of_white_frame)[0] < number_of_frame:
    print("[ERROR] in STEP 2")
temp = np.array(i)
set_of_white_frame.sort(key=sort_func)

for position, white_frame in set_of_white_frame:
    white_frame = cv2.resize(white_frame, (final_width, final_height))
    cv2.imshow("Detected white frame", white_frame)

    # cv2.imwrite("detect.jpg", white_frame)
    # STEP 3: Determine the coordinate of the Grid
    threshold_grid = process_image.determine_threshold_for_grid(white_frame)
    process_image.set_threshold(threshold_grid)

    line1, line2, ver_coor, translation = process_image.detect_grid_coodinate(white_frame)


    # STEP 4: Find center point
    cX, cY = process_image.find_center_point(white_frame)
    if cX == -1:
        print("[ERROR] in STEP 4")


    # STEP 5: Calculate the real coordinate of the laser pointer
    distance_x = process_image.calculate_real_coordinate_of_laser_pointer(cX, cY, ver_coor)
    print("Khoang cach: " + str(distance_x))
    temp = np.insert(temp, 0, distance_x)
    output_image_file = "Outputs/LAB/May18/TEST/image/" + image_name

    # STEP 6: Draw and Save image
    final_image = process_image.shift_image(white_frame, translation)
    font = cv2.FONT_HERSHEY_COMPLEX
    for j in range(15):
        cv2.line(final_image, (line1[j][0] + translation, line1[j][1]), (line2[j][0], line2[j][1]),
                 (0, 0, 0), 1)

    cv2.circle(final_image, (cX, cY), 5, (0, 0, 255), 1, cv2.LINE_AA)
    cv2.line(final_image, (cX, cY), (ver_coor[0], cY), (0, 0, 255), 1)
    cv2.putText(final_image, str(distance_x) + 'cm', (int(cX / 2), cY - 10), font, 0.5, (255, 0, 0))
    final_img_size = np.shape(final_image)

    final_image = cv2.resize(src=final_image[:, abs(translation):final_img_size[1] - abs(translation), :],
                             dsize=(final_width, final_height))
    cv2.imshow("Processed image", final_image)
    cv2.waitKey(0)
    cv2.imwrite(output_image_file, final_image)


print(temp)
cv2.waitKey(0)



