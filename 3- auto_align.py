# //read excel sheet
from functions import *
from stats_gen import *
from manipulate import *
import matplotlib as plt
from os import getcwd


detections = read_excel(getcwd() + "/montage_report/excels/1689177310.xlsx")


#straighten images of faces
# entry = detections[0]
for entry in detections:

    # //determine eye EYE_ANGLE
	left, right, angle = find_eye_angle(entry.left_eye_detection,entry.right_eye_detection)
	rotated = rotate(entry.file,angle)
	cv2.imshow("rotated_image", rotated)
	cv2.waitKey(0)



	# if eye angle is negative rotate right
    # else rototate left
# align(entry)

