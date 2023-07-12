# import matplotlib.pyplot as mp
from stats_gen import *
from functions import *
from os import getcwd
import cv2

detections = read_excel(getcwd() + "/montage_report/excels/1689155462.xlsx")
left,right,angle = find_eye_angle(detections[0].left_eye_detection,detections[0].right_eye_detection)
image = cv2.imread(detections[0].file)
print(left,right,angle)
cv2.circle(image,left, 1, (100,100,0), 1)
cv2.circle(image,right, 1, (100,100,0), 1)
cv2.line(image,left,right,(100,100,0), 1)

cv2.imshow("middle of eyes",image)
cv2.waitKey(0)
# x_axis =  [i for i in range(0,100,2)]
# y_axis = [ i for i in range(50)]
# print(x_axis)
# print(y_axis)

# mp.plot(x_axis,y_axis)
# mp.show()