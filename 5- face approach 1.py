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

def get_outline(entry_image):
	# edge detection
	edges = cv2.cvtColor(entry_image, cv2.COLOR_BGR2GRAY)
	#blur image
	edges = cv2.GaussianBlur(edges,(7,7),0)
	#detect edges

	edges = edges[0:math.floor(edges.shape[0]*0.85),0:edges.shape[1]]

	edges = cv2.Canny(edges,50,50)
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


	new_outline = np.zeros(outline.shape,dtype=np.uint8)

	for col in range(1,outline.shape[1]):
		for row in range(1,outline.shape[0]):
			pixel = edges[row][col]
			if pixel != 0:
				new_outline[row][col] = 255
				# front_array.append((row,col))
				break

	final_outline = cv2.bitwise_or(outline,new_outline)

	return final_outline


def get_bounds(entry_outline):
	x_array, y_array = [],[]

	for r in range(entry_outline.shape[0]):
		for c in range(entry_outline.shape[1]):
			# smallest x
			pixel = entry_outline[r][c]
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

	return (smallest_x, smallest_y, largest_x, largest_y)


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

	final_outline = get_outline(proc_img)
	proc_img = proc_img[0:math.floor(proc_img.shape[0]*0.85),0:proc_img.shape[1]]
	smallest_x,smallest_y,largest_x,largest_y = get_bounds(final_outline)


	left_pad = smallest_x
	right_pad = final_outline.shape[1] - largest_x
	top_excess = smallest_y
	area = (largest_x - smallest_x) * (largest_y - smallest_y)
	# new_height = 500
	# new_width = (new_height * final_outline.shape[0]) / final_outline.shape[1]
	# print("183 size before",proc_img.shape)
	new_image = proc_img#cv2.resize(proc_img,(int(new_height),int(new_width)))
	print("proc and outline shapes",proc_img.shape[:2] , new_image.shape[:2])
	# print("185 size after",new_image.shape)
	# cv2.imshow("outline",final_outline)
	# cv2.waitKey(0)


	images.append((new_image,area))


# sort images by area
images = sorted(images,key=lambda x: x[1])
middle_area = images[len(images)//2][1]
# resize images to middle area
for index in range(len(images)):
	current = images[index]
	area = current[1]
	ratio = middle_area / area
	if ratio != 1: # if the area aren't the same resize the image
		new_area = area * ratio
		new_height, new_width = current[0].shape[:2]
		new_height *= ratio
		new_width *= ratio
		print("206 size before",current[0].shape)
		new_image = cv2.resize(current[0], (int(new_height),int(new_width)))
		print("208 size after",new_image.shape)
		images[index] = (new_image,new_area)



#crop top padding
excess_list = []
for index in range(len(images)):
	current = images[index]
	img = current[0]
	outline = get_outline(img)
	small_x,small_y,large_x,large_y = get_bounds(outline)
	excess_list.append((smallest_y, index, smallest_x, largest_y))
# sort excess_list according to smallest_y
excess_list = sorted(excess_list,key=lambda x: x[0])

crop_val = excess_list[0][0]
pad_val = min(sorted(excess_list,key=lambda x:x[2])[0][2],   sorted(excess_list,key=lambda x:x[3])[0][3])

for element in excess_list:
	element_padding = element[0]
	im_index = element[1]
	if crop_val < element_padding:
		#crop top of main image
		start = element_padding - crop_val

		images[im_index] = (images[im_index][0][start:][:],images[im_index][1])
	element_padding = element[2]
	#left crop
	if element_padding > pad_val:
		images[im_index] = (images[im_index][0][:][pad_val:],images[im_index][1])
		#crop by smallest horizontal
	# right crop
	element_padding = element[3]
	if element_padding > pad_val:
		images[im_index] = (images[im_index][0][:][:-pad_val],images[im_index][1])

min_x,min_y = 0,0

# find the smallest width
for entry in images:
	im = entry[0]
	if min_y < entry[0].shape[1]:
		min_x,min_y = entry[0].shape[:2]

for index in range(len(images)):
	shape = images[index][0].shape
	if min_x != shape[0] or min_y != shape[1]:
		print("256 size before",images[index][0].shape)
		images[index] = (cv2.resize(images[index][0], (min_y,min_x)), images[index][1])
		print("258 size after",images[index][0].shape)
		print('min shape',(min_x,min_y),'current shape',shape)

	print("shapes",index,images[index][0].shape)
# concatenate images side by side
montage = np.concatenate([x[0] for x in images],axis=1)
cv2.imwrite("final.jpg",montage)































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