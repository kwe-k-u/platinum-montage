import os
import sys
import tkinter as tk
from tkinter import filedialog
import cv2
from PIL import Image, ImageTk

parent = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parent)
from functions import *
from stats_gen import *
from manipulate import *
from detection_class import detection



path = "C:/Users/KWAKU/Desktop/Platinum Dental/Montage maker/pictures\IMG_0499.JPG"


#get image

report = generate_report([path])
detector = detector()
detection = detection(report[0])
selected = detector.gen_mesh(path)



_, _, angle = find_eye_angle(selected.left_eye_detection,selected.right_eye_detection)

result = rotate(selected.file,angle)


#show result
result = cv2.resize(result, (300,250))
selected.image = cv2.resize(selected.image, (300,250))
# cv2.imshow("initial", selected.image)
# cv2.waitKey(0)
# cv2.imshow("cv result", result)
# cv2.waitKey(0)