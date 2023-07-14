import numpy as np
import cv2
from random import randint
import matplotlib.pyplot as mp

def find_area(cordinates):
	# new_cords = cordinates.copy()
	# new_cords.append(cordinates[0])

	total = 0
	first = None
	second = None

	for i in cordinates:
		# print(i)
		if first is None:
			first = i
			continue
		# elif second is None:
		# 	second = i
		else:
			second = i

		# print(total + (first[0]*second[1]) - (first[1]*second[0]))
		value =  (first[1]*second[0]) - (first[0]*second[1])
		# print(first,second, value)
		total = total + value
		# print(first[0],"*",second[1],"-",first[1],"*",second[0],"=", value)
		first = second

	first = second
	second = cordinates[0]
	# print(first[0],"*",second[1],"-",first[1],"*",second[0],"=", value)
	total = total + (first[0]*second[1]) - (first[1]*second[0])
	return total/2



def show_points(detection):
    print("preparing to show points")
    for i in range(len(detection)):
        # print(i,"detections")
        cords = []
        detect = detection[i]
        image = np.zeros((600,600,3),dtype=np.uint8)
        # image = np.zeros((detect.img_width,detect.img_height,3),dtype=np.uint8)
        cords = detect.left_eye_detection
        # print(cords)
        # input("waiting")
        cords.extend(detect.right_eye_detection)
        # cords.extend(detect.lip_detection)
        # cords.extend(detect.face_detection)
        # cords.extend(detect.nose_detection)
        col = (256,256,256)#(randint(1,100),randint(1,100),50)
        for point in cords:
	        # point times 10 for enlargement
            cv2.circle(image, (point[0]%500,point[1]%500), 4 , col, -1)

        cv2.imshow("detect.file",image)
        cv2.waitKey(0)



# 	RIGHT EYE
# l- 33[7]
# r- 133[0]
# t- 159[11]
# b- 145[4]

# LEFT EYE
# l- 362[7]
# r- 263[0]
# t- 386[11]
# b- 374[4]
#Gives the angle that the eyes in the image are tilted
#The left eye is the anchor. If left is negative, right is positive
# returns (left_mid,right_mid,angle)
def find_eye_angle(left_cord,right_cord):
	# determinate the point at which the landmarks intercept
	def middle(line1, line2):
		xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
		ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

		# Determinant
		def det(a, b):
			return a[0] * b[1] - a[1] * b[0]

		div = det(xdiff, ydiff)

		d = (det(*line1), det(*line2))
		x = det(d, xdiff) // div
		y = det(d, ydiff) // div
		return x, y

	left_hor = (left_cord[7],left_cord[0]); # right eye horizontal
	left_vert = (left_cord[11],left_cord[4]); # left eye vertical

	right_hor = (right_cord[7],right_cord[0]); # righteye horizontal line
	right_vert = (right_cord[11],right_cord[4]); # right eye vertical line

	left_mid = middle(left_hor,left_vert)
	right_mid = middle(right_hor,right_vert)

	#eye line = ((x1,y1), (x2,y2))
	# eye_angle = (left_mid, right_mid)
	delta_x = left_mid[0] - right_mid[0]
	delta_y = left_mid[1] - right_mid[1]
	#normal_line = ((x1,y1), ())
	# normal_angle = (left_mid), (right_mid[0],left_mid[1])
	angle = np.arctan(delta_y / delta_x)

        # Converting radians to degrees
	angle = (angle * 180) / np.pi
	return  left_mid,right_mid,angle







def graph_face_ratio(detections):
	def find_face_percentage(face_cords,img_heigth,img_width):
		face_area = find_area(face_cords)
		image_area = img_width*img_heigth #find_area([(1,1),(img_width,1),(1,img_heigth),(img_width,img_heigth)])
		print("area",face_area,image_area)

		percentage = (face_area//image_area)
		return percentage

	ratios = {}
	# mp.figure(figsize=(200,150))
	for entry in detections:
		value = find_face_percentage(entry.face_detection,entry.img_height,entry.img_width)
		if(ratios.get(value) == None):
			ratios[value] = 1
		else:
			ratios[value] += 1

	x_vals = []
	y_vals = []
	for x in ratios:
		x_vals.append(x)
		y_vals.append(ratios[x])
		# print(x,ratios[x])
	mp.scatter(x_vals,y_vals,color='green', linestyle='dashed', linewidth = 3, marker='o', markerfacecolor='blue', markersize=12)

	# mp.tight_layout()
	mp.show()



# def graph_face_angles(detections):
# 	for entry in detections:
# 		angle = find_eye_angle(entry.left_eye_detection,entry.right_eye_detection)
# 		pass


def aspect_ratio(width, height):
	return width/height