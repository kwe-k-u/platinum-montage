import os
import re
from openpyxl import Workbook
# import detector
from detector import detector
from time import time

# //================INDEXES FOR THE POSITION OF STATISTIC DATA
EYE_ANGLE = 1# - Angle of eyes
LIP_ANGLE = 2# - Angle of lips
FACE_TO_IMAGE = 3# - Ratio of face to image
CENTER_CORDINATES = 4# - Center Cordinates of face?
LEFT_EYE = 5# - left eye position
RIGHT_EYE = 6# -right eye position


def find_images(directory):
    image_extensions = ['.jpg', '.jpeg', '.png']
    image_files = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            _, extension = os.path.splitext(file)
            if extension.lower() in image_extensions:
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

    for row in data[0]:
        is_edited = edited(row)
        general_sheet.append([row, "edited" if is_edited else "unedited" ])
        if is_edited:
            edited_sheet.append([row])
        else:
            unedited_sheet.append([row])




    # Save the workbook
    name = int(time())
    workbook.save('C:\\Users\\KWAKU\\Desktop\Platinum Dental\\Montage maker\\montage_maker\\excels\\'+str(name)+'.xlsx')
    pass


def generate_report():
    pass























# folder_path = input("Drag and drop the folder here: ")
directory_to_search ="C:\\Users\\KWAKU\\Desktop\Platinum Dental\\Montage maker\\test folder";
directory_to_search = re.sub(r"(?<!/)/(?!/)", "//", directory_to_search)
# Call the function to find images
found_images = find_images(directory_to_search)

# //run the detector on the find_images
module = detector()
module.detect(found_images[1])
# face_cords = module.find_left_eye(found_images[0])
# face_cords = module.find_right_eye(found_images[0])
# face_cords = module.find_mouth(found_images[0])
# face_cords = module.find_face(found_images[0])
# face_cords = module.find_other(found_images[0])
# module



# generate report
# write_excel([found_images])
