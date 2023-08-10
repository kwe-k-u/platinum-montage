import cv2
from stats_gen import *
import math


# def align(image):
#     # left,right,angle = find_eye_angle(image.left_eye_detection,image.right_eye_detection)
#     if(angle > 0):
#         # rotate()
#         pass

def rotate(path, angle):

    def right_crop(matrix):
        top_left, bottom_right, top_right,bottom_left = None, None, None, None
        im_height,im_width = matrix.shape[:2]
        threshold= 1

        for row in range(im_height):
            #stop looping if the top crop point has been found
            if top_left  is not None:
                break
            for col in range(im_width):
                pixel = matrix[row][col]
                if pixel[0] > threshold and pixel[1] > threshold and pixel[2] > threshold:
                    top_left = (row,col)
                    break

        for row in range(im_height-1,0,-1):
            if bottom_right is not None:
                break
            for col in range (im_width-1,0,-1):
                pixel = matrix[row][col]
                if pixel[0] > threshold and pixel[1] > threshold and pixel[2] > threshold:
                    bottom_right = (row,col)
                    break

        cropped_image = matrix[top_left[0]:bottom_right[0],top_left[1]:bottom_right[1]]
        im_height, im_width = cropped_image.shape[:2]


        for col in range(im_width-1,0,-1):
            if top_right is not None:
                break
            for row in range(im_height):
                pixel = cropped_image[row][col]
                if pixel[0] > threshold and pixel[1] > threshold and pixel[2] > threshold:
                    top_right = row
                    break

        for col in range(im_width):
            if bottom_left is not None:
                break
            for row in range(im_height-1,0,-1):
                pixel = cropped_image[row][col]
                if pixel[0] > threshold and pixel[1] > threshold and pixel[2] > threshold:
                    bottom_left = row
                    break
        if top_right is not None and bottom_left is not None:
            cropped_image = cropped_image[top_right:bottom_left][:]
        elif top_right is None and bottom_left is not None:
            cropped_image = cropped_image[:bottom_left][:]
        elif top_right is not None and bottom_left is None:
            cropped_image = cropped_image[top_right:][:]


        return cropped_image
        #find index for top right crop



    def left_crop(matrix):
        return matrix
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
    rot_height, rot_width,_ = rotated_mat.shape
    # set height and width to match index
    rot_height -= 1
    rot_width -= 1

    rotated_mat = right_crop(rotated_mat)

    if angle < 0 : # head is tilted right if angle is negative
        rotated_mat = right_crop(rotated_mat)
    else:
        rotated_mat = left_crop(rotated_mat)

    return rotated_mat



def crop_img(image):
    return image
# y=0
# x=0
# h=100
# w=200
# crop = image[y:y+h, x:x+w]
