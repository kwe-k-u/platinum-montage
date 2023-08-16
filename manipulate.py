import cv2
from stats_gen import *
import math


# def align(image):
#     # left,right,angle = find_eye_angle(image.left_eye_detection,image.right_eye_detection)
#     if(angle > 0):
#         # rotate()
#         pass

def rotate(image, angle):

    def right_crop(matrix):
        top_left, bottom_right, top_right,bottom_left = None, None, None, None
        im_height,im_width = matrix.shape[:2]
        threshold= 1

        #top to bottom
        for row in range(im_height):
            #stop looping if the top crop point has been found
            if top_left is not None and bottom_right is not None:
                break
            #left to right
            for col in range(im_width):
                #top left marker
                pixel = matrix[row][col]
                if top_left is None:
                    if pixel[0] > threshold and pixel[1] > threshold and pixel[2] > threshold:
                        top_left = (row,col)

                # bottom right marker
                if bottom_right is None and row != 0 and col != 0:
                    pixel = matrix[-row][-col]
                    if pixel[0] > threshold and pixel[1] > threshold and pixel[2] > threshold:
                        bottom_right = (-row,-col)


                #stop looping if all markers have been found
                if bottom_right is not None and top_left is not None:
                    break



        cropped_image = matrix[top_left[0]:bottom_right[0],top_left[1]:bottom_right[1]]
        im_height, im_width = cropped_image.shape[:2]


        # left to right
        for col in range(im_width):
            if bottom_left is not None and top_right is not None:
                break
            # top to bottom
            for row in range(im_height):
                if top_right is not None and bottom_left is not None:
                    break
                if top_right is None and col != 0:
                    pixel = cropped_image[row][-col]
                    if pixel[0] > threshold and pixel[1] > threshold and pixel[2] > threshold:
                        top_right = row

                if bottom_left is None and row != 0:
                    pixel = cropped_image[-row][col]
                    if pixel[0] > threshold and pixel[1] > 0 and pixel[2] > threshold:
                        bottom_left = -row








        print(top_left,bottom_left,top_right,bottom_right)
        if top_right is not None and bottom_left is not None:
            cropped_image = cropped_image[top_right:bottom_left][:]
        elif top_right is None and bottom_left is not None:
            cropped_image = cropped_image[:bottom_left][:]
        elif top_right is not None and bottom_left is None:
            cropped_image = cropped_image[top_right:][:]


        return cropped_image
        #find index for top right crop



    def left_crop(matrix):
        top_left, bottom_left,top_right,bottom_right = None,None,None,None
        im_height,im_width = matrix.shape[:2]
        threshold= 1
        #top to bottom
        for row in range(im_height):
            if top_right is not None and bottom_left is not None:
                break
            #right to left
            for col in range(im_width):
                if top_right is None and col != 0:
                    pixel = matrix[row][-col]
                    if pixel[0] > threshold and pixel[1] > threshold and pixel[2] > threshold:
                        top_right = (row,-col)

                if bottom_left is None and row != 0:
                    pixel = matrix[-row][col]
                    if pixel[0] > threshold and pixel[1] > threshold and pixel[2] > threshold:
                        bottom_left = (-row,col)

        cropped_image = matrix[top_right[0]:bottom_left[0],bottom_left[1]:top_right[1]]
        im_height,im_width = cropped_image.shape[:2]

        for col in range(im_width):
            if top_left is not None and bottom_right is not None:
                break
            for row in range(im_height):
                if top_left is not None and bottom_right is not None:
                    break
                if top_left is None:
                    pixel = cropped_image[row][col]
                    if pixel[0] > threshold and pixel[1] > threshold and pixel[2] > threshold:
                        top_left = row

                if bottom_right is None and col != 0 and row != 0:
                    pixel = cropped_image[-row][-col]
                    if pixel[0] >threshold and pixel[1] > threshold and pixel[2] > threshold:
                        bottom_right = -row

                # for row in range(im_width):




        print(top_left,bottom_left,top_right,bottom_right)
        if top_left is not None and bottom_right is not None:
            cropped_image = cropped_image[top_left:bottom_right][:]
        elif top_left is not None and bottom_right is None:
            cropped_image = cropped_image[top_left:][:]
        elif top_left is None and bottom_right is not None:
            cropped_image = cropped_image[:bottom_right][:]
        return cropped_image


    # image = cv2.imread(path)
    #rotate the image
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
    print(angle)
    # rotated_mat = right_crop(rotated_mat)

    if angle < 0 : # head is tilted right if angle is negative
        print("right crop")
        rotated_mat = right_crop(rotated_mat)
    else:
        print('left crop')
        rotated_mat = left_crop(rotated_mat)
    resized = cv2.resize(rotated_mat,(500,500))
    return rotated_mat



