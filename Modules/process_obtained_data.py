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




file_name = "../Outputs/example_video/2/excelFolder/time-distance.xlsx"
x, y = load_data_from_excel_file(file_name)
data = calculate_parameters(x, y)
print(data)