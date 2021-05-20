from turtledemo.__main__ import font_sizes

import xlrd
import numpy as np
import matplotlib.pyplot as plt
import argparse

# construct the argument parse and parse the arguments
# ap = argparse.ArgumentParser()
# ap.add_argument("-p", "--presult",
#                 help="path to the (optional) images file")  # mở đường dẫn tệp image có sẵn
# args = vars(ap.parse_args())
#
# # Give the location of the file
# filename = "Evaluation_results_for_chart/"+args["presult"]+".xlsx"
filename_1 = 'Outputs/LAB/May18/TEST/11.1.xlsx'
filename_2 = 'Outputs/LAB/May18/TEST/8.1.xlsx'
# To open Workbook
wb = xlrd.open_workbook(filename_1)
sheet = wb.sheet_by_index(0)
time_1 = []
location_1 = []
j = 1
# For row 0 and column 0
for i in range(1, sheet.nrows):
    # time.append(sheet.cell_value(i, 0))
    x_temp = sheet.cell_value(i, 1)
    if x_temp == '':
        print("Cell %d: Blank" % (i))
        continue
    time_1.append(j)
    location_1.append(x_temp)
    j += 1


# location = np.array(location).astype(np.float)
location_avg_1 = round(np.average(location_1), 2)
location_avg_1 = np.ones(int(max(time_1)))*location_avg_1
line_min_1 = np.ones(int(max(time_1)))*min(location_1)
line_max_1 = np.ones(int(max(time_1)))*max(location_1)

# To open Workbook
wb = xlrd.open_workbook(filename_2)
sheet = wb.sheet_by_index(0)
time_2 = []
location_2 = []
j = 1
# For row 0 and column 0
for i in range(1, sheet.nrows):
    # time.append(sheet.cell_value(i, 0))
    x_temp = sheet.cell_value(i, 1)
    if x_temp == '':
        print("Cell %d: Blank" % (i))
        continue
    time_2.append(j)
    location_2.append(x_temp)
    j += 1

time = len(time_1) if len(time_1) < len(time_2) else len(time_2)

print(time)
location_avg_2 = round(np.average(location_2), 2)
location_avg_2 = np.ones(int(max(time_2)))*location_avg_2
line_min_2 = np.ones(int(max(time_2)))*min(location_2)
line_max_2 = np.ones(int(max(time_2)))*max(location_2)

plt.figure(figsize=(10,4))
healthy_volunteer = plt.plot(time_1[:time], location_1[:time] - location_avg_1[:time], color='blue', linestyle='dashed', linewidth=1,
         marker='o', markerfacecolor='blue', markersize=2)
patient = plt.plot(time_2[:time], location_2[:time] - location_avg_2[:time], color='red', linestyle='dashed', linewidth=1,
         marker='o', markerfacecolor='red', markersize=2)

plt.legend((healthy_volunteer[0], patient[0]), ('Healthy Volunteer', 'Patient'))

# max1 = plt.plot(time_1[:time], line_max_1[:time] - location_avg_1[:time], color='black', linestyle='dashed')
# min1 = plt.plot(time_1[:time], line_min_1[:time] - location_avg_1[:time], color='black', linestyle='dashed')
#
# max2 = plt.plot(time_2[:time], line_max_2[:time] - location_avg_2[:time], color='black', linestyle='dashed')
# min2 = plt.plot(time_2[:time], line_min_2[:time] - location_avg_2[:time], color='black', linestyle='dashed')
plt.xlabel('Video Frame')
plt.ylabel('Distance(cm)')
plt.grid(True)

# plt.title('The Chart Compares the Change between Healthy Volunteer and Patient')
plt.show()

