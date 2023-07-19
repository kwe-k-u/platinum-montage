import os
import sys
import tkinter as tk
from tkinter import filedialog
import cv2
from PIL import Image, ImageTk

parent = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parent)
from functions import *
from stats_gen import *
from manipulate import *
from detection_class import detection


class PageTwo(tk.Frame):
	def __init__(self, parent, folder_path, switch_to_page_one):
		super().__init__(parent)
		self.parent = parent
		self.title("Select images")

			# Get the image file paths in the folder
		image_files = []
		for filename in os.listdir(folder_path):
			if is_image(filename):
				image_files.append(os.path.join(folder_path, filename))

		self.selected_images = []

		def toggle_image_selection(image_index):
			if image_files[image_index] in self.selected_images:
				self.selected_images.remove(image_files[image_index])
			else:
				self.selected_images.append(image_files[image_index])
		# Create a grid of images
		row = 0
		col = 0
		for i in range(len(image_files)):
			image_file = image_files[i]
			# Read the image using cv2
			img = cv2.imread(image_file)
			# Convert the image from BGR to RGB
			img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
			# Resize the image to a smaller size (optional)
			img = cv2.resize(img, (200, 200))

			# Convert the image to Tkinter-compatible format
			img = Image.fromarray(img)
			img_tk = ImageTk.PhotoImage(img)

			# Create a label to display the image
			# label = tk.Label(self.root, image=img_tk)
			# label.grid(row=row, column=col, padx=10, pady=10)
			checkbox = tk.Checkbutton(self.root,variable=tk.BooleanVar(),
									  command=lambda idx=i: toggle_image_selection(idx)
									  )
			checkbox.img = img_tk
			checkbox.config(image=img_tk)
			checkbox.grid(row=row, column=col,padx=10,pady=10)


			# Store the image label to prevent garbage collection
			# label.image = img_tk

			# Update the row and column indices
			col += 1
			if col == 4:
				col = 0
				row += 1

		change_folder_button = tk.Button(self.root, text="Change directory<Not working>", command= self.open_folder_dialog)
		change_folder_button.grid(row=(len(image_files) // 4) + 3, column=0, columnspan=2, pady=10)

		detect_face_button = tk.Button(self.root, text="Detect Face", command=self.detection_window)
		detect_face_button.grid(row=(len(image_files) // 4) + 3, column=2, columnspan=2)

