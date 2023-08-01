import os as o
import re
from functions import *

# Prepare environment for scanning
# Create a folder in the current directory to work from
cwd = o.getcwd()
# Create a folder for the excel sheet and a report on the images detected
o.makedirs(cwd + "/montage_report/excels/",511,True)
o.makedirs(cwd + "/montage_report/logs/",511,True)
# input("wait")

# the folder that contains the images we want to generate a report on
directory_to_search ="C:\\Users\\KWAKU\\Desktop\Platinum Dental\\Montage maker\\pictures";
directory_to_search = re.sub(r"(?<!/)/(?!/)", "//", directory_to_search) # cleaning the path of escape characters


# get the path for all images with faces (generate log of fails)
# images = find_images(directory_to_search)
images = ["C:\\Users\\KWAKU\\Desktop\\Platinum Dental\\Montage maker\\pictures\\IMG_0506.JPG"]
# images = ["C:\\Users\\KWAKU\\Desktop\\Platinum Dental\\Montage maker\\pictures\\IMG_0500.JPG"]
# module = detector()

# for file in images:
# 	print("generating report for " + file)
# 	img = cv2.imread(file)
# 	img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
# 	temp = module.gen_mesh(file)
# 	if temp == None:
# 		print("no face detected")
# 		continue

# 	# left = module.detect_left_eye()
# 	right = module.detect_right_eye()
# 	nose = module.detect_nose_eye()
# 	lips = module.detect_lips_eye()
# 	# print("left",left)
# 	print("right",right)
# 	print("nose",nose)
# 	print("lips",lips)




import argparse
import cv2

def detect_faces(image_path):
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Unable to load the image.")
        return

    # Load pre-trained face detection model
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    # Convert the image to grayscale for face detection
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Draw rectangles around the detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    h,w,_ = image.shape
    image = cv2.resize(image, (w//3,h//3))
    # image = cv2.resize(image, (0,0), fx=0.5, fy=0.5)
    # Display the image with face detections
    cv2.imshow("Face Detections", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Create an argument parser
    # parser = argparse.ArgumentParser(description="Face detection on an image using argparse.")
    # parser.add_argument("image_path", type=str, help="Path to the input image")

    # # Parse the arguments
    # args = parser.parse_args()

    # Perform face detection on the input image
    detect_faces(images[0])

