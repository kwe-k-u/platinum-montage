import os
import sys
import tkinter as tk
from tkinter import filedialog
import cv2
from PIL import Image, ImageTk

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from functions import *

class MontageMakerApp:
	def __init__(self):
		self.root = tk.Tk()
		self.root.title("Montage Maker")
		self.folder_path = ""

		# Montage Maker label
		self.montage_label = tk.Label(self.root, text="Montage maker", font=("Helvetica", 24))
		self.montage_label.pack(pady=20)

		# Folder selection components
		self.folder_frame = tk.Frame(self.root)
		self.folder_frame.pack()

		self.folder_entry = tk.Entry(self.folder_frame, width=30)
		self.folder_entry.pack(side=tk.LEFT)

		self.select_folder_button = tk.Button(self.folder_frame, text="Select Folder", command=self.open_folder_dialog)
		self.select_folder_button.pack(side=tk.LEFT)

		# Submit button
		self.submit_button = tk.Button(self.root, text="Submit", command=self.select_image_window)
		self.submit_button.pack(pady=20)

	def run(self):
		# Centering the window
		window_width = 400
		window_height = 200
		screen_width = self.root.winfo_screenwidth()
		screen_height = self.root.winfo_screenheight()
		x_coordinate = int((screen_width/2) - (window_width/2))
		y_coordinate = int((screen_height/2) - (window_height/2))
		self.root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_coordinate, y_coordinate))

		self.root.mainloop()

	def open_folder_dialog(self):
		folder_path = filedialog.askdirectory()
		if folder_path:
			self.folder_path = folder_path
			self.folder_entry.delete(0, tk.END)
			self.folder_entry.insert(tk.END, folder_path)

	def detect_face(self):
		pass



	def select_image_window(self):
		def change_folder():
			new_window.destroy()
			self.root.deiconify()
		folder_path = self.folder_entry.get()
		self.root.destroy()  # Close the current window
		new_window = tk.Tk()
		new_window.title("Select images")

		# Retrieve the folder path from the previous window

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
		# print(image_files)
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
			# label = tk.Label(new_window, image=img_tk)
			# label.grid(row=row, column=col, padx=10, pady=10)
			checkbox = tk.Checkbutton(new_window,variable=tk.BooleanVar(),
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

		change_folder_button = tk.Button(new_window, text="Change directory", command= change_folder)
		change_folder_button.grid(row=(len(image_files) // 4) + 3, column=0, columnspan=2, pady=10)

		detect_face_button = tk.Button(new_window, text="Detect Face", command=self.detect_face)
		detect_face_button.grid(row=(len(image_files) // 4) + 3, column=2, columnspan=2)


		new_window.mainloop()


# Create and run the MontageMakerApp instance
app = MontageMakerApp()
app.run()
