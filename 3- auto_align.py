# //read excel sheet
from functions import *
from stats_gen import *
from manipulate import *
import matplotlib as plt
from os import getcwd


detections = read_excel(getcwd() + "/montage_report/excels/1689155462.xlsx")


#straighten images of faces
for entry in detection:
    align(entry)

