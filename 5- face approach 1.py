import os
import cv2
import numpy as np
import sys
import multiprocessing

parent = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parent)
from functions import *
from stats_gen import *
from manipulate import *
from detection_class import detection

def get_outline(entry_image, path = None):
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
	if path is None:
		return final_outline
	return (path,final_outline, entry_image)


def get_bounds(entry_outline, proc_img = None):
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
	if proc_img is None:
		return (smallest_x, smallest_y, largest_x, largest_y)

	return (smallest_x, smallest_y, largest_x, largest_y, proc_img)

def get_detections(path, index = None):
		try:
			report = generate_report([path])[0]
			detect = detection(report)
			_,_,angle = find_eye_angle(detect.left_eye_detection,detect.right_eye_detection)
			proc_img = rotate(detect.image,angle)
		except:
			proc_img = cv2.imread(path)
		if index is None:
			return proc_img
		return proc_img, index


# Creates a new thread
# extra_data => information that needs to be paired with the result, returned as a spread
def spin_thread(func,args = [],result_queue = None):
	print("starting new process")
	result = func(*args)
	if result_queue is not None:
		result_queue.put(result)


if __name__ == "__main__":
	files = ["IMG_0500.JPG","IMG_0499.JPG","IMG_0501.JPG","IMG_0503.JPG","IMG_0504.JPG"]
	files = ["C:\\Users\\KWAKU\\Desktop\\Platinum Dental\\Montage maker\\pictures\\"+x for x in files]
	images = []
	detection_model = detector()
	# =========================================[START] Process Set One =================================================

	#create different threads for each file scan
	process_list = [] # list of threads for file detection processes
	process_queue = multiprocessing.Queue() #queue for first thread list
	process_results = [] #list of results from first queue

	for file_index in range(len(files)):
		path = files[file_index]
		process = multiprocessing.Process(target=spin_thread, args = (get_detections,[path,file_index],process_queue))
		process_list.append(process)
		process.start()

	while len(process_results) != len(process_list):
		result = process_queue.get()
		process_results.append(result)

	# cv2.destroyWindow("proc res")
	for process in process_list:
		process.join()
	# =========================================[END] Process Set One =================================================

	process_list = []
	process_results = sorted(process_results, key=lambda x : x[1])


	# =========================================[START] Process Set Two =================================================
	process_queue = multiprocessing.Queue()
	for proc_img,_ in process_results:
		path = files[_]
		process = multiprocessing.Process(target=spin_thread,args =(get_outline,[proc_img,path],process_queue))
		process_list.append(process)
		process.start()

	process_results = []

	while len(process_results) != len(process_list):
		result = process_queue.get()
		process_results.append(result)

		# cv2.waitKey(0)
		#wait for files to be read
	for process in process_list:
		process.join()
	process_two_results = process_results
	# =========================================[END] Process Set Two =================================================
	process_list = []
	process_results = []

	# =========================================[START] Process Set Three =================================================
	process_queue = multiprocessing.Queue()

	for path_index in range(len(files)):
		path = files[path_index]
		final_outline = None
		for p,o,proc_img in process_two_results:
			if p == path:
				final_outline = o
				break
		if final_outline is None:
			raise Exception("Final outline not provided")


		proc_img = proc_img[0:math.floor(proc_img.shape[0]*0.85),0:proc_img.shape[1]]
		process = multiprocessing.Process(target=spin_thread, args=(get_bounds,[final_outline,proc_img],process_queue))
		process_list.append(process)
		process.start()
	while len(process_list) != len(process_results):
		result = process_queue.get()
		process_results.append(result)

	for process in process_list:
		process.join()
	# =========================================[END] Process Set Three =================================================

	for smallest_x,smallest_y,largest_x,largest_y, proc_img in process_results:
		# smallest_x,smallest_y,largest_x,largest_y = get_bounds(final_outline)

		left_pad = smallest_x
		right_pad = final_outline.shape[1] - largest_x
		top_excess = smallest_y
		area = (largest_x - smallest_x) * (largest_y - smallest_y)


		images.append((proc_img,area))


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
			new_image = cv2.resize(current[0], (int(new_height),int(new_width)))
			images[index] = (new_image,new_area)



	# ================================kk=========[START] Process Set  =================================================
	#crop top padding
	excess_list = []
	for index in range(len(images)):
		current = images[index]
		img = current[0]
		outline = get_outline(img)
		small_x,small_y,large_x,large_y = get_bounds(outline)
		excess_list.append((smallest_y, index, smallest_x, largest_y))

	# ==========================kk===============[END] Process Set One =================================================
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
			images[index] = (cv2.resize(images[index][0], (min_y,min_x)), images[index][1])

	# concatenate images side by side
	print("images length", len(images))
	montage = np.concatenate([x[0] for x in images],axis=1)
	cv2.imwrite("final.jpg",montage)

