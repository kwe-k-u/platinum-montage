import os
from openpyxl import Workbook, open as open_excel
# import detector
from  detection_class import detection
from detector import detector
from time import time
import cv2
import numpy as np
import math
from manipulate import rotate
from stats_gen import find_eye_angle


from PIL import Image, ImageTk

cwd = os.getcwd()

def is_image(path):
    image_extensions = ['.jpg', '.jpeg', '.png']
    _, extension = os.path.splitext(path)
    return extension.lower() in image_extensions



def find_images(directory):
    image_files = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            if is_image(file):
                image_files.append(os.path.join(root, file))


    return image_files


def write_excel(data):

    #returns a boolean indicated if an image is edited (file_name ends in an A) or unedited

    def edited(path):
        _, extension = os.path.splitext(path)
        return _[-1].lower() == "a"


    # Create a new workbook
    workbook = Workbook()
    general_sheet = workbook.active #information about all types of images
    unedited_sheet = workbook.create_sheet(title='Undited')# information about editied images
    edited_sheet = workbook.create_sheet(title='Edited')#information about unedited images

    # Set the delimiter to ;
    general_sheet.csv_delimiter = ';'
    edited_sheet.csv_delimiter = ';'
    unedited_sheet.csv_delimiter = ';'

    # Add data to the sheet

    for row in data:
        is_edited = edited(row[0])
        general_sheet.append(row)
        if is_edited:
            edited_sheet.append(row)
        else:
            unedited_sheet.append(row)




    # Save the workbook
    name = int(time())
    workbook.save(cwd+'/montage_report\\excels\\'+str(name)+'.xlsx')

# Creates a log file for images that did not have faces (failed detection)
def write_to_log(file_name):
    file = open(cwd+"/montage_report/logs/failed_detect.log","a")
    file.write(file_name+"\n")
    file.close()


def generate_report(file_names):
    # print("file_names "+ str(len(file_names)))

    module = detector() #feature detector
    data = []

    for file in file_names:
        try:
            print("generating report for "+ file)
            img = cv2.imread(file)
            img = cv2.flip(img,1)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # //if image has multiple faces skip it
            # funcd = dlib.get_frontal_face_detector()
            # num_faces = funcd(img)
            # if len(num_faces) != 1:
            #     pass
            module.gen_mesh(file)

            img_height = img.shape[0]
            img_width = img.shape[1]

            left_eye_cords = module.detect_left_eye()
            right_eye_cords = module.detect_right_eye()
            face_cords = module.detect_face()
            lips_cords = module.detect_lips()
            nose_cords = module.detect_nose()
            # module.show(nose_cords)

            row = [file,img_height,img_width]
            temp = []
            temp.extend(left_eye_cords)
            temp.extend(right_eye_cords)
            temp.extend(lips_cords)
            temp.extend(face_cords)
            temp.extend(nose_cords)

            for val in temp:
                if (type(val) == type((0,0))): #if value is a tuple, split it
                    row.extend([val[0],val[1]])
                else:
                    row.append(val)
            data.append(row)
        except Exception as e:
            #list the traceback types
            m=""
            print(e.with_traceback(m))
            print(m)

            print("file failed  "+ file)
            write_to_log(file)
            pass

    return data


# returns of detection objects from the read excel sheet
# true for edited detections
# false for unedited detections
def read_excel(filename, edited = False) -> list:
    data = []
    workbook = open_excel(filename)
    if(edited):
        sheet = workbook.get_sheet_by_name("Edited")
    else:
        sheet = workbook.get_sheet_by_name("Undited")
    # work = Workbook()
    # work.get_sheet_by_name("").iter_rows()
    print("reading")
    for row in sheet.iter_rows():
        # detect =
        data.append(detection(row))
        # if(len(data) > 5):
        #     print("previs",data[-1].left_eye_detection[0],data[-3].left_eye_detection[0])
    # print("comapris", data[0].left_eye_detection == data[2].left_eye_detection)
    return data

def resize_image(image,nh = 100):
    if type(image) == type(""):
        img = cv2.imread(image)
    else:
        img = image
    nw = int((nh*img.shape[1])/img.shape[0])
    result = cv2.resize(img,(nw,nh))
    return result
# def resize_image(image,seed_width = 100):
#     if type(image) == type(""):
#         img = cv2.imread(image)
#     else:
#         img = image
#     nh = int(img.shape[1]*(seed_width/img.shape[0]))
#     img = cv2.resize(img, (nh, seed_width))
#     return img


#creates a tk image object for the ui
def create_tk_image(image):
    resized_image = image
    im = Image.fromarray(resized_image)
    img_tk = ImageTk.PhotoImage(im)
    return img_tk





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


def top_crop(ob,start,index):
	cropped = (ob[0][start:][:],ob[1])
	return (cropped,index)


def left_crop(ob,pad_val,index):
	cropped = (ob[0][:][pad_val:],ob[1])
	return (cropped,index)

def right_crop(obj,pad_val,index):
	# cropped = (ob[0][:][pad_val:],ob[1])
	cropped = (obj[0][:][:-pad_val],obj[1])
	return (cropped,index)

# Creates a new thread
# extra_data => information that needs to be paired with the result, returned as a spread
def spin_thread(func,args = [],result_queue = None):
	print("starting new process")
	result = func(*args)
	if result_queue is not None:
		result_queue.put(result)

















# detections = read_excel("C:\\Users\\KWAKU\\Desktop\\Platinum Dental\\Montage maker\\montage_maker\\excels\\1688999966.xlsx")
# print(len(detections))
# folder_path = input("Drag and drop the folder here: ")
# directory_to_search ="C:\\Users\\KWAKU\\Desktop\Platinum Dental\\Montage maker\\test folder"
# directory_to_search = re.sub(r"(?<!/)/(?!/)", "//", directory_to_search)
# # Call the function to find images
# found_images = find_images(directory_to_search)
# # print(found_images[0])
# # generate_report(found_images)
# print("found images ",len(found_images))
# report = generate_report(found_images)
# # write_excel(report)

# //run the detector on the find_images



# generate report
# write_excel([found_images])
