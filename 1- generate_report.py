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
images = find_images(directory_to_search)
# get cordinates for facial landmarks
report_data = generate_report(images)
#create excel sheet with the information
write_excel(report_data)