import os
import xlsxwriter

if not os.path.exists("Outputs/data/1/1_1/X/excelFolder/time-distance.xlsx"):
    workbook = xlsxwriter.Workbook("Outputs/data/1/1_1/X/excelFolder/time-distance.xlsx")
    worksheet = workbook.add_worksheet('result')
    worksheet.write_row(0, 0, ['Frame', 'X(cm)', 'Y(cm)'])
    workbook.close()