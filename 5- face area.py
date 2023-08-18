import os
import cv2
import numpy as np
import sys

parent = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parent)
from functions import *
from stats_gen import *
from manipulate import *
from detection_class import detection




files = ["IMG_0500.JPG","IMG_0499.JPG","IMG_0501.JPG","IMG_0503.JPG","IMG_0504.JPG"]
files = ["C:\\Users\\KWAKU\\Desktop\\Platinum Dental\\Montage maker\\pictures\\"+x for x in files]
images = []
detection_model = detector()
for path in files:
	try:
		report = generate_report([path])[0]
		detect = detection(report)
		_,_,angle = find_eye_angle(detect.left_eye_detection,detect.right_eye_detection)
		# print(angle)
		proc_img = rotate(detect.image,angle)
		# detect = detection_model.gen_mesh(detect)
		# detect.image = proc_img
	except:
		proc_img = cv2.imread(path)

	# images.append(proc_img)


	# edge detection
	edges = cv2.cvtColor(proc_img, cv2.COLOR_BGR2GRAY)
	#blur image
	edges = cv2.GaussianBlur(edges,(7,7),0)
	#detect edges

	edges = edges[0:math.floor(edges.shape[0]*0.85),0:edges.shape[1]]

	edges = cv2.Canny(edges,50,50)
	# edges = cv2.resize(edges,(500,500))


	# black image size of edges
	outline = np.zeros(edges.shape,dtype=np.uint8)
	# front_array, back_array = [],[]

	# keep only the fist and last horizontal detection
	for row in range(1,edges.shape[0],3): #top to bottom
		back,front = None,None
		for col in range(1,edges.shape[1]//2): #left to right
			if front is None:
				pixel = edges[row][col]
				if pixel != 0:
					front = (row,col)
			if back is None:
				pixel = edges[row][-col]
				if pixel != 0:
					back = (row,-col)

			if front is not None and back is not None:
				outline[front[0]][front[1]] = 255
				outline[back[0]][back[1]] = 255
				break


	# front_array.extend(back_array)




	# for pint in front_array:
	# 		outline[pint[0]][pint[1]] = 255

	threshold = 100

	new_outline = np.zeros(outline.shape,dtype=np.uint8)

	for col in range(1,outline.shape[1]):
		for row in range(1,outline.shape[0]):
			pixel = edges[row][col]
			if pixel != 0:
				new_outline[row][col] = 255
				# front_array.append((row,col))
				break

	final_outline = cv2.bitwise_or(outline,new_outline)
	# array of 10% smallest x values
	x_array, y_array = [], []
	for r in range(final_outline.shape[0]):
		for c in range(final_outline.shape[1]):
			# smallest x
			pixel = final_outline[r][c]
			if pixel > 0:
				x_array.append(c)
				y_array.append(r)

	x_array.sort()
	y_array.sort()
	x_10_percent,y_10_percent = len(x_array) // 10, len(y_array) // 10
	smallest_x = sum(x_array[:x_10_percent])//len(x_array[:x_10_percent])
	smallest_y = sum(y_array[:y_10_percent])//len(y_array[:y_10_percent])
	largest_y = sum(y_array[-y_10_percent:])//len(y_array[-y_10_percent:])
	largest_x = sum(x_array[-x_10_percent:])//len(x_array[-x_10_percent:])

	area = (largest_x - smallest_x) * (largest_y - smallest_y)
	new_height = 500
	new_width = (new_height * final_outline.shape[0]) / final_outline.shape[1]
	final_outline = cv2.resize(final_outline,(int(new_width),int(new_height)))
	cv2.imshow("outline",final_outline)
	cv2.waitKey(0)
-

	images.append((final_outline,area))


# resize images to the same area but maintain aspect ratios
# images = sorted(images,key=lambda x: x[1])
# mid_img, mid_area = images[len(images)//2]

# for img, area in images:
# 	if (area > mid_area):
# 		img = cv2.resize(img,(mid_img.shape[1],mid_img.shape[0]))
# 	elif (area < mid_area):
# 		mid_img = cv2.resize(mid_img,(img.shape[1],img.shape[0]))


# images.reverse()
# outline = np.concatenate([x[0] for x in images],axis=1)
# cv2.imwrite("final.jpg",outline)


# outline_n = np.concatenate([x[0] for x in images],axis=1)
# put outline below outline_n
# outline = np.concatenate([outline_n,mid_img],axis=0)


# cv2.imwrite("resized.jpg",outline)
# w = (outline.shape[0] * h) // outline.shape[1]
# outline.resize((w,h))
# cv2.imshow("edited",outline)
# cv2.waitKey(0)