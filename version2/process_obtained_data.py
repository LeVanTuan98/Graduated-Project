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
    # y = []
    # For row 0 and column 0
    for i in range(1, sheet.nrows):
        x.append(sheet.cell_value(i, 1))
        # y.append(sheet.cell_value(i, 2))
    x = np.array(x)
    # y = np.array(y)
    X = x - x.mean()
    # Y = y - y.mean()
    return X


def load_parameters_from_excel_file(file_name):
    wb = xlrd.open_workbook(file_name)
    sheet = wb.sheet_by_index(0)
    name = []
    MV = []
    RMS = []
    MD = []
    # For row 0 and column 0
    for i in range(1, sheet.nrows):
        name.append(sheet.cell_value(i, 0))
        MV.append(sheet.cell_value(i, 2))
        RMS.append(sheet.cell_value(i, 3))
        MD.append(sheet.cell_value(i, 4))

    return name, MV, RMS, MD


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


def draw_graph_between_2_group(data, type="MV"):
    STT = np.arange(1, np.size(data) + 1)
    volunteer_data = data[0:35]
    patient_data = data[35:39]

    volunteer_avg = round(np.average(volunteer_data), 2)
    volunteer_std = round(np.std(volunteer_data), 2)

    patient_avg = round(np.average(patient_data), 2)
    patient_std = round(np.std(patient_data), 2)

    # data_plot = plt.figure(figsize=(30, 15))
    if type == "MV":
        MV_plot = plt.figure()
        plt.title('Mean Velocity')
        # plt.xlabel('STT')
        plt.ylabel('MV(cm/s)')
    elif type == "RMS":
        RMS_plot = plt.figure()
        plt.title('Root Mean Square Distance')
        # plt.xlabel('STT')
        plt.ylabel('RMS')
    elif type == "MD":
        MD_plot = plt.figure()
        plt.title('Mean Distance')
        # plt.xlabel('STT')
        plt.ylabel('MD(cm)')

    volunteer = plt.stem(STT[0:35], volunteer_data)
    patient = plt.stem(STT[35:39], patient_data, linefmt='red', markerfmt='C3o')

    volunteer_avg_line = plt.plot(STT[0:35], np.ones(np.size(STT[0:35])) * volunteer_avg, color='green')
    volunteer_std_line = plt.plot(STT[0:35], np.ones(np.size(STT[0:35])) * (volunteer_avg + volunteer_std),
                                  color='black', linestyle='dashed')
    volunteer_std_line = plt.plot(STT[0:35], np.ones(np.size(STT[0:35])) * (volunteer_avg - volunteer_std),
                                  color='black', linestyle='dashed')

    patient_avg_line = plt.plot(STT, np.ones(np.size(STT)) * patient_avg, color='orange')
    patient_std_line = plt.plot(STT, np.ones(np.size(STT)) * (patient_avg + patient_std), color='black',
                                linestyle='dashed')
    patient_std_line = plt.plot(STT, np.ones(np.size(STT)) * (patient_avg - patient_std), color='black',
                                linestyle='dashed')

    plt.legend((volunteer[0], patient[0], volunteer_avg_line[0], patient_avg_line[0]),
               ('Healthy volunteers', 'Patients', "Mean of healthy volunteers", "Mean of patients"),
               loc="upper left", ncol=2)

    plt.grid(True)
    plt.ylim([0, 3])
    plt.show()


def compared_amplitude_between_2_groups(volunteer_data, patient_data):
    video_frame = np.arange(1, np.size(volunteer_data) + 1)

    plt.figure(figsize=(10, 4))
    healthy_volunteer = plt.plot(video_frame, volunteer_data, color='blue', linestyle='dashed', linewidth=1,
                                 marker='o', markerfacecolor='blue', markersize=2)
    patient = plt.plot(video_frame, patient_data, color='red', linestyle='dashed',linewidth=1,
                       marker='o', markerfacecolor='red', markersize=2)

    plt.legend((healthy_volunteer[0], patient[0]), ('Healthy Volunteer', 'Patient'))

    plt.xlabel('Video Frame')
    plt.ylabel('Distance(cm)')
    plt.grid(True)

    plt.title('The Chart Compares the amplitude between Healthy Volunteer and Patient')
    plt.show()


file_name_1 = "Outputs/LAB/May18/TEST/11.1.xlsx"
file_name_2 = "Outputs/LAB/May18/TEST/8.1.xlsx"
volunteer_data = load_data_from_excel_file(file_name_1)
patient_data = load_data_from_excel_file(file_name_2)
compared_amplitude_between_2_groups(volunteer_data, patient_data)

file_name = "Outputs/LAB/May18/TEST/34volun_3pati.xlsx"
name, MV, RMS, MD = load_parameters_from_excel_file(file_name)
draw_graph_between_2_group(MD, type="MD")
draw_graph_between_2_group(RMS, type="RMS")



