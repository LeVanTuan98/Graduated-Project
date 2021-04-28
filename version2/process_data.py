import xlrd
import numpy as np


excel_file_path = "Resourses/sample.xlsx"
wb = xlrd.open_workbook(excel_file_path)
sheet = wb.sheet_by_index(0)
x = []
y = []

for i in range(1, sheet.nrows):
    x.append(sheet.cell_value(i, 5))
    y.append(sheet.cell_value(i, 6))

x = np.array(x)
y = np.array(y)
mean_x = np.mean(x)
mean_y = np.mean(y)
X = x - mean_x
Y = y - mean_y


# Number of sample (N)
N = len(X)

# Resultant distance (RD)
RD = np.sqrt(X ** 2 + Y ** 2)

# Mean Distance (MD)
MD = np.mean(RD)

# Root mean square distance (RMS_dis)
RMS_dis = np.sqrt((np.sum(RD ** 2)) / N)

# Total path
total_path = 0
for i in range(N - 1):
    total_path += np.sqrt((X[i + 1] - X[i]) ** 2 + (Y[i + 1] - Y[i]) ** 2)

# Mean velocity (MV)
times = N/30
MV = total_path/times

# Area CC (area_cc)
z = 1.645
RD_std = np.std(RD)
area_cc = np.pi * ((MD + RD_std * z) ** 2)

# Area CE (area_ce)
X_std = np.std(X)
Y_std = np.std(Y)
XY_std = np.std(X * Y)
F = 3.00
area_ce = F * np.sqrt(X_std ** 2 + Y_std ** 2 - XY_std ** 2)

# Sway area (sw)
total = 0
for i in range(N - 1):
    total += abs(X[i + 1] * Y[i] + X[i] * Y[i + 1])

sw = total / (2 * times)

# Mean frequency
f = MV / (2 * np.pi * MD)

print("length Data: ", N)
print("MV: ", MV)
print("RMS: ", RMS_dis)
print("total_path", total_path)
print("Mean velocity", MV)
print("Area CC", area_cc)
print("Area CE", area_ce)
print("Sway area", sw)

