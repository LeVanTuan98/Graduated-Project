from process_functions import *

final_width = 620
final_height = 180
pre_line1 = 0
pre_line2 = 0
pre_ver_coor = 0
distance_x = 0

image_name = '40.jpg'
input_image_file = "../Inputs/experiment_images//raw_images/" + image_name

process_image = Process()

# STEP 1: Load image
original_image = cv2.imread(input_image_file)
# cv2.imshow("Original image", cv2.resize(src=original_image, dsize=(500, 200)))

# STEP 2: Detect WHITE frame
white_frame = process_image.detect_white_frame(original_image)
if white_frame.shape == original_image.shape:
    print("[ERROR] in STEP 2")

white_frame = cv2.resize(white_frame, (np.shape(white_frame)[1]*2, np.shape(white_frame)[0]*2))
# cv2.imshow("Detected white frame", white_frame)

# cv2.imwrite("detect.jpg", white_frame)
# STEP 3: Determine the coordinate of the Grid
threshold_grid = process_image.determine_threshold_for_grid(white_frame)
process_image.set_threshold(threshold_grid)

line1, line2, ver_coor, translation = process_image.detect_grid_coodinate(white_frame)

if np.size(ver_coor) != 15:
    threshold_grid = process_image.determine_threshold_for_grid(white_frame)
    process_image.set_threshold(threshold_grid)

    # STEP 4: Determine the coordinate of the Grid - Lap lai buoc 4
    line1, line2, ver_coor, translation = process_image.detect_grid_coodinate(white_frame)

    if np.size(ver_coor) != 15:
        line1 = pre_line1
        line2 = pre_line2
        ver_coor = pre_ver_coor
        if np.size(pre_ver_coor) != 15:
            print("[ERROR] in STEP 3")

pre_line1 = line1
pre_line2 = line2
pre_ver_coor = ver_coor

# STEP 4: Find center point
cX, cY = process_image.find_center_point(white_frame)
if cX == -1:
    print("[ERROR] in STEP 4")


# STEP 5: Calculate the real coordinate of the laser pointer
distance_x = process_image.calculate_real_coordinate_of_laser_pointer(cX, cY, ver_coor)
print("Khoang cach: " + str(distance_x))


output_image_file = "../Inputs/experiment_images/processed_images/" + image_name

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
cv2.imwrite(output_image_file, final_image)
cv2.waitKey(0)
cv2.destroyAllWindows()



