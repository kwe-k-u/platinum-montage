# //read excel sheet
from functions import *
from stats_gen import *
import matplotlib as plt
from os import getcwd


detections = read_excel(getcwd() + "/montage_report/excels/1689155462.xlsx")
# show_points(detections)
graph_face_ratio(detections)
# graph_face_angles(detections)




# // plot all the detection points  (face)
#  Option two : graph of these metrics
# === UNEDITED - face
# - Angle of eyes
# - Angle of lips
# - Ratio of face to image
# - Center Cordinates of face?
# - left eye position
# -right eye position

# === EDITED - face
# - Angle of eyes
# - Angle of lips
# - Ratio of face to image
# - Center cordinates of face?
# - right eye position
# - left eye position


# - Size of image
# - distance of left eye from edge
# - distance of right right from edge