import cv2
from stats_gen import *
import math


# def align(image):
#     # left,right,angle = find_eye_angle(image.left_eye_detection,image.right_eye_detection)
#     if(angle > 0):
#         # rotate()
#         pass

def rotate(path, angle):
    image = cv2.imread(path)
    height, width = image.shape[:2]
    image_center = (width / 2, height / 2)

    new_image = cv2.getRotationMatrix2D(image_center, angle, 1)

    radians = math.radians(angle)
    sin = math.sin(radians)
    cos = math.cos(radians)
    bound_w = int((height * abs(sin)) + (width * abs(cos)))
    bound_h = int((height * abs(cos)) + (width * abs(sin)))

    new_image[0, 2] += ((bound_w / 2) - image_center[0])
    new_image[1, 2] += ((bound_h / 2) - image_center[1])

    rotated_mat = cv2.warpAffine(image, new_image, (bound_w, bound_h))
    return rotated_mat

    cv2.imshow("rotated image", rotated_mat)
    cv2.waitKey(0)


def crop(detection, new_img):
    image = detection.image
# y=0
# x=0
# h=100
# w=200
# crop = image[y:y+h, x:x+w]

    pass