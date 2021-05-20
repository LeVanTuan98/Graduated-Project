import xlrd
import xlsxwriter
import openpyxl
import numpy as np
import matplotlib.pyplot as plt
import os
import glob


def load_data_from_excel_file(file_name):
    wb = xlrd.open_workbook(file_name)
    sheet = wb.sheet_by_index(0)
    x = []
    y = []
    # For row 0 and column 0
    for i in range(1, sheet.nrows):
        x.append(sheet.cell_value(i, 1))
        y.append(sheet.cell_value(i, 2))
    x = np.array(x)
    y = np.array(y)
    X = x - x.mean()
    Y = y - y.mean()
    return X, Y

def load_data_from_scale_excel_file(file_name):
    wb = xlrd.open_workbook(file_name)
    sheet = wb.sheet_by_index(0)
    x = []
    y = []
    # For row 0 and column 0
    for i in range(1, sheet.nrows):
        f1 = sheet.cell_value(i, 0)
        f2 = sheet.cell_value(i, 1)
        f3 = sheet.cell_value(i, 2)
        f4 = sheet.cell_value(i, 3)
        if (f1 + f2 + f3 + f4) != 0:
            x.append(round(((f3 + f4) - (f1 + f2)) * 15.2 / (f1 + f2 + f3 + f4), 2))
            y.append(round(((f1 + f4) - (f2 + f3)) * 18.9 / (f1 + f2 + f3 + f4), 2))
    x = np.array(x)
    y = np.array(y)
    X = x - x.mean()
    Y = y - y.mean()
    return X, Y


def calculate_parameters(X, Y):
    # Number of samples
    N = len(X)

    # Resultant distance (RD)
    RD = np.sqrt(X ** 2 + Y ** 2)

    # Mean Distance (MD)
    MD = RD.mean()

    # Root mean square distance (RMS dis)
    RMS = np.sqrt((np.sum(RD ** 2)) / N)

    # Total Path
    total_path = 0
    for i in range(N - 1):
        total_path += np.sqrt((X[i + 1] - X[i]) ** 2 + (Y[i + 1] - Y[i]) ** 2)

    # Mean Velocity (MV)
    times = N / 30
    MV = total_path / times

    # Area CC
    z = 1.645
    s = np.std(RD)
    area_CC = np.pi * (MD + z *s)

    # Area CE
    sx = np.std(X)
    sy = np.std(Y)
    sxy = np.std(X * Y)
    F = 3.00
    area_CE = F * np.sqrt(sx**2 + sy**2 - sxy**2)

    # Sway area (Sw)
    sum_temp = 0
    for i in range(N - 1):
        sum_temp += abs(X[i + 1] * Y[i] + X[i] * Y[i + 1])
    Sw = sum_temp / (2 * times)

    # Mean frequency (f)
    f = MV / (2 * np.pi * MD)

    return [N, MD, RMS, MD, area_CC, area_CE, Sw, f]


def compare_data_by_graph(video_x, video_y, scale_x, scale_y, option="All"):
    times = np.arange(0, len(video_x)) / 30
    time_scale = np.linspace(0, len(video_x), len(scale_x)) / 30

    if option == "XY":
        XY_plot = plt.figure()

        video = plt.plot(video_x, video_y, color='blue', linestyle='none',
                         marker='o', markerfacecolor='blue', markersize=5)

        scale = plt.plot(scale_x, scale_y, color='red', linestyle='none',
                         marker='o', markerfacecolor='red', markersize=5)
        plt.title('The graph shows the data correlation between video and scale')
        plt.xlabel('X(cm)')
        plt.ylabel('Y(cm)')

        plt.legend((video[0], scale[0]), ('Data from video', 'Data from scale'))
        plt.grid(True)
    elif option == "Y":
        Y_plot = plt.figure()
        video = plt.plot(times, video_y, color='blue', linestyle='dashed')

        scale = plt.plot(time_scale, scale_y, color='red', linestyle='dashed')

        plt.xlabel('Time(s)')
        plt.ylabel('Distance(cm)')
        plt.title('Y Axis')
        plt.legend((video[0], scale[0]), ('Data from video', 'Data from scale'))
        plt.grid(True)
    elif option == "X":
        X_plot = plt.figure()
        video = plt.plot(times, video_x, color='blue', linestyle='dashed')

        scale = plt.plot(time_scale, scale_x, color='red', linestyle='dashed')

        plt.xlabel('Time(s)')
        plt.ylabel('Distance(cm)')
        plt.title('X Axis')
        plt.legend((video[0], scale[0]), ('Data from video', 'Data from scale'))
        plt.grid(True)
    elif option == "All":
        XY_plot = plt.figure()

        video = plt.plot(video_x, video_y, color='blue', linestyle='none',
                         marker='o', markerfacecolor='blue', markersize=5)

        scale = plt.plot(scale_x, scale_y, color='red', linestyle='none',
                         marker='o', markerfacecolor='red', markersize=5)
        plt.title('The graph shows the data correlation between video and scale')
        plt.xlabel('X(cm)')
        plt.ylabel('Y(cm)')

        plt.legend((video[0], scale[0]), ('Data from video', 'Data from scale'))
        plt.grid(True)
#==========================
        Y_plot = plt.figure()
        video = plt.plot(times, video_y, color='blue', linestyle='dashed')

        scale = plt.plot(time_scale, scale_y, color='red', linestyle='dashed')

        plt.xlabel('Time(s)')
        plt.ylabel('Distance(cm)')
        plt.title('Y Axis')
        plt.legend((video[0], scale[0]), ('Data from video', 'Data from scale'))
        plt.grid(True)
#============================
        X_plot = plt.figure()
        video = plt.plot(times, video_x, color='blue', linestyle='dashed')

        scale = plt.plot(time_scale, scale_x, color='red', linestyle='dashed')

        plt.xlabel('Time(s)')
        plt.ylabel('Distance(cm)')
        plt.title('X Axis')
        plt.legend((video[0], scale[0]), ('Data from video', 'Data from scale'))
        plt.grid(True)

    plt.show()


file_name = "../Outputs/LAB/April24/Khanh/2/excelFolder/time-distance.xlsx"
video_x, video_y = load_data_from_excel_file(file_name)
# data = calculate_parameters(video_x, video_y)
# print(data)
file_name = "../Outputs/LAB/April24/Khanh/2/excelFolder/Can.xlsx"
scale_x, scale_y = load_data_from_scale_excel_file(file_name)
compare_data_by_graph(video_x, video_y, scale_x, scale_y, option="All")

