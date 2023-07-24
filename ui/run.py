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

class MontageMakerApp:
	def __init__(self):
		self.select_folder_window(False)

	def select_folder_window(self, existing = True):
		if(existing):
			self.root.destroy()
		self.root = tk.Tk()
		self.root.title("Montage Maker")
		self.folder_path = ""
		self.detection_list = []
		self.show_marks = True

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


	# Window 2
	def select_image_window(self):

		def toggle_image_selection(image_index):
			if image_files[image_index] in self.selected_images:
				self.selected_images.remove(image_files[image_index])
			else:
				self.selected_images.append(image_files[image_index])

		folder_path = self.folder_entry.get()
		self.root.destroy()  # Close the current window
		self.root = tk.Tk()
		self.root.title("Select images")

		# Retrieve the folder path from the previous window

		# Get the image file paths in the folder
		image_files = []
		for filename in os.listdir(folder_path):
			if is_image(filename):
				image_files.append(os.path.join(folder_path, filename))

		self.selected_images = []

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

		change_folder_button = tk.Button(self.root, text="Change directory", command= self.select_folder_window)
		change_folder_button.grid(row=(len(image_files) // 4) + 3, column=0, columnspan=2, pady=10)

		detect_face_button = tk.Button(self.root, text="Detect Face", command=self.detection_window)
		detect_face_button.grid(row=(len(image_files) // 4) + 3, column=2, columnspan=2)


		self.root.mainloop()

	# Window 3
	def detection_window(self, index = 0):
		# def change_current_image(image_path):
		# 	# l.image = img
		# 	# img = cv2.imread(image_path)
		# 	# img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
		# 	# img_tk = ImageTk.PhotoImage(img)
		# 	# image_label = tk.Label(middle_frame, image=img_tk)
		# 	# # image_label.image = img_tk
		# 	# image_label.pack()
		# 	pass

		if(len(self.selected_images) == 0):
			self.select_image_window()
			return 0

		def straigthen():
			selected = self.detection_list[index]
			left, right, angle = find_eye_angle(selected.left_eye_detection,selected.right_eye_detection)
			rotated = rotate(selected.file,angle)
			self.show_marks = False

			self.detection_list[index].image = rotated

			self.detection_window(index)

		def toggle_marks():
			self.show_marks = not self.show_marks
			self.detection_window(index)

		def crop_16_9():
			self.window_crop(self.detection_list[index])
			# self.window_crop(self.detection_list[index].image)
			# cropper = ImageCropperApp(self.detection_list[index].image,onCropListener)
			# pass
		def onCropListener(image):
			cv2.imshow("cropped",image)
			cv2.waitKey(0)

		def reset_image():
			report = generate_report([self.detection_list[index].file])
			self.detection_list[index] = detection(report[0])
			self.show_marks = True
			self.detection_window(index)


		def ai_crop():
			selected = self.detection_list[index]
			cropped = crop_img(selected.file)
			self.show_marks = False

			self.detection_list[index].image = cropped

			self.detection_window(index)



		self.root.destroy()  # Close the second window
		self.root = tk.Tk()
		self.root.title("Image Detection")

		# First frame to hold the images from the second page
		first_frame = tk.Frame(self.root)
		first_frame.pack(pady=10, side="left")

		# Middle frame to display the image
		middle_frame = tk.Frame(self.root)
		middle_frame.pack(pady=10, side="left")

		# Third frame for the detection buttons
		third_frame = tk.Frame(self.root)
		third_frame.pack(pady=10, side="left")

		# Retrieve the folder path from the previous window
		# self.detection_list = []
		if(len(self.detection_list) == 0):
			for f in self.selected_images:
				detection_row = generate_report([f])
				detect = detection(detection_row[0])
				self.detection_list.append(detect)

		# Create a grid of images in the first frame
		row = 0
		col = 0
		for i in range(len(self.detection_list)):

			#PERFORMING DETECTIONS
			# detector = detector()

			img =  self.detection_list[i].get_marked_img()
			# detector.gen_mesh(image_file)
			# Read the image using cv2
			# img = cv2.imread(image_file)
			# Convert the image from BGR to RGB

			img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
			# Resize the image to a smaller size (optional)
			img = cv2.resize(img, (100, 100))


			# Convert the image to Tkinter-compatible format
			img = Image.fromarray(img)
			img_tk = ImageTk.PhotoImage(img)


			# Create a label to display the image
			label = tk.Button(first_frame,image=img_tk,
			  command=lambda idx=i : self.detection_window(idx)
			  )
			label.image = img_tk
			label.grid(row=row, column=col, padx=10, pady=10)

			# Update the row and column indices
			col += 1
			if col == 1:
				col = 0
				row += 1


		# Display the selected image in the middle frame
		detect = self.detection_list[index]

		if(self.show_marks):
			img = detect.get_marked_img()
		else:
			img = detect.image

		img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
		img = Image.fromarray(img)
		img_tk = ImageTk.PhotoImage(img)
		image_label = tk.Label(middle_frame, image=img_tk)
		# image_label.image = img_tk
		image_label.pack()

		# Detection buttons in the third frame
		face_button = tk.Button(third_frame, text="AI Straigthen", command=straigthen)
		face_button.pack(pady=5)

		left_eye_button = tk.Button(third_frame, text="AI Crop", command=ai_crop)
		left_eye_button.pack(pady=5)

		left_eye_button = tk.Button(third_frame, text="Manual Crop", command=crop_16_9)
		left_eye_button.pack(pady=5)


		reset_button = tk.Button(third_frame, text="Reset image", command=reset_image)
		reset_button.pack(pady=5)


		show_mark_button = tk.Button(third_frame, text="Toggle marking", command=lambda: toggle_marks() )
		show_mark_button.pack(pady=5)

		show_montage_button = tk.Button(third_frame, text="Create montage", command=self.create_montage_img)
		show_montage_button.pack(pady=5)


		self.root.mainloop()




	# Window 4
	def window_crop(self,detection):


		def show_image():
			# Resize the image to fit the label
			h, w, _ = detection.image.shape
			max_height = 600
			max_width = 800
			if h > max_height or w > max_width:
				scale = min(max_height / h, max_width / w)
				self.image = cv2.resize(detection.image, (int(w * scale), int(h * scale)))

			image_rgb = cv2.cvtColor(detection.image, cv2.COLOR_BGR2RGB)
			image_tk = ImageTk.PhotoImage(Image.fromarray(image_rgb))
			self.image_label.config(image=image_tk)
			self.image_label.image = image_tk
			self.image_label.pack()
			self.confirm_button.config(state=tk.NORMAL)
			self.confirm_button.pack(pady=10)

		def toggle_mode():
			if self.crop_mode == "custom":
				self.crop_mode = "16:9"
				self.toggle_button.config(text="Switch to Custom Mode")
				self.page_label.config(text="16:9 Mode: Click to draw a cropping frame")
			else:
				self.crop_mode = "custom"
				self.toggle_button.config(text="switch to 16:9 Mode")
				self.page_label.config(text="Custom Mode: Click and drag to draw a cropping frame")

			show_image_with_cropping_frame()

		def on_mouse_press(event):
			self.crop_start = (event.x, event.y)

		def on_mouse_drag(event):
			if self.crop_start:
				self.crop_rect = (self.crop_start[0], self.crop_start[1], event.x, event.y)
				show_image_with_cropping_frame()

		def on_mouse_release( event):
			self.crop_start = None

		def show_image_with_cropping_frame():
			image_with_frame = detection.image.copy()

			if self.crop_mode == "16:9":
				h, w, _ = image_with_frame.shape
				aspect_ratio =  9/ 16
				crop_width = int(h * aspect_ratio)

				# Center the cropping frame around the click (if in 16:9 mode)
				if self.crop_rect and self.crop_start:
					cx = (self.crop_rect[0] + self.crop_rect[2]) // 2
					cy = (self.crop_rect[1] + self.crop_rect[3]) // 2
					self.crop_rect = (cx - crop_width // 2, cy - h // 2, cx + crop_width // 2, cy + h // 2)

				dark_tint = np.zeros(image_with_frame.shape, dtype=np.uint8)
				dark_tint.fill(50)  # Darken the tint

				# Apply the dark tint to the areas outside the cropping frame
				image_with_frame = np.where(dark_tint > image_with_frame, dark_tint, image_with_frame)

			if self.crop_rect:
				cv2.rectangle(image_with_frame, (self.crop_rect[0], self.crop_rect[1]),
							(self.crop_rect[2], self.crop_rect[3]), (255, 0, 0), 2)

			image_rgb = cv2.cvtColor(image_with_frame, cv2.COLOR_BGR2RGB)
			image_tk = ImageTk.PhotoImage(Image.fromarray(image_rgb))
			self.image_label.config(image=image_tk)
			self.image_label.image = image_tk

		def crop_image():
			if self.crop_rect:
				x1, y1, x2, y2 = self.crop_rect
				detection.image = detection.image[y1:y2, x1:x2]
				#get detection index
				detection_index = self.detection_list.index(detection)
				self.detection_window(detection_index)



		# self.image =image
		# folder_path = self.folder_entry.get()
		self.root.destroy()  # Close the current window
		self.root = tk.Tk()
		self.root.title("Crop images")
		self.crop_rect = None
		self.crop_start = None
		self.crop_mode = "16:9"  # or "custom"
		self.page_label = tk.Label(self.root, text="16:9 Mode: Click to draw a cropping frame", font=("Helvetica", 16))
		self.page_label.pack(pady=10)
		# Image label to display the loaded image
		self.image_label = tk.Label(self.root)
		self.image_label.pack()

		# Toggle button to switch between custom and 16:9 modes
		self.toggle_button = tk.Button(self.root, text="16:9 Mode", command=toggle_mode)
		self.toggle_button.pack()

		# Confirm button to crop the image
		self.confirm_button = tk.Button(self.root, text="Confirm", command=crop_image)
		self.confirm_button.pack(pady=10)
		# self.confirm_button.config(state=tk.DISABLED)  # Disable until image loaded

		# Bind mouse events to the image label
		self.image_label.bind("<ButtonPress-1>", on_mouse_press)
		self.image_label.bind("<B1-Motion>", on_mouse_drag)
		self.image_label.bind("<ButtonRelease-1>", on_mouse_release)

		show_image()
		self.root.mainloop()

	# Window 5
	def create_montage_img(self):
		montage_order = []

		def update_montage_image():
			#if montage_order is empty show a black image
			if len(montage_order) == 0:
				self.montage = np.zeros((400, 400, 3), np.uint8)
				img = Image.fromarray(self.montage)
				img_tk = ImageTk.PhotoImage(img)
				self.montage_image_label.config(image=img_tk)
				self.montage_image_label.image = img_tk

			#get images from self.detection_list by indexes in montage_order
			#create one image with all the images side by side
			else:
				images = []
				for i in montage_order:
					mon_image = self.detection_list[i].image;
					mon_image = cv2.cvtColor(mon_image, cv2.COLOR_BGR2RGB)
					mon_image = cv2.resize(mon_image, (250, 250))
					images.append(mon_image)


				#concatenate images
				self.montage = np.concatenate(images, axis=1)

				montage = Image.fromarray(self.montage)
				montage_tk = ImageTk.PhotoImage(montage)
				self.montage_image_label.config(image=montage_tk)
				self.montage_image_label.image = montage_tk

		def toggle_image_selection(image_index):
			#if image hasn't been selected add it to the image image above
			if image_index not in montage_order:
				montage_order.append(image_index)
			else: #remove index from montage order
				montage_order.remove(image_index)

			update_montage_image()

		def save_montage():
			#save the detection list images in montage folder
			for i in self.detection_list:
				#change name from img.ext to imgA.ext
				parts = i.file.split(".")
				new_name = ".".join(parts[:-1]) + "a." + parts[-1]
				cv2.imwrite("montage/"+new_name, i.image)

			#save montage to file
			montage = cv2.cvtColor(self.montage, cv2.COLOR_BGR2RGB)
			cv2.imwrite("montage/montage.jpg", montage)

			#open montage in new window
			os.system("montage/montage.jpg")


		self.root.destroy()
		self.root = tk.Tk()
		self.root.title("Create montage")


		top_frame = tk.Frame(self.root)
		top_frame.pack(side=tk.TOP)

		botom_frame = tk.Frame(self.root)
		botom_frame.pack(side=tk.BOTTOM)

		action_frame = tk.Frame(self.root)
		action_frame.pack(side=tk.BOTTOM)



		self.montage_image_label = tk.Label(top_frame)
		img = np.zeros((250, 250, 3), np.uint8)
		img = Image.fromarray(img)
		img_tk = ImageTk.PhotoImage(img)
		self.montage_image_label.config(image=img_tk)
		self.montage_image_label.image = img_tk
		self.montage_image_label.pack()

		i = 0
		for detection in self.detection_list:
			checkbox = tk.Checkbutton(botom_frame, variable=tk.BooleanVar(),
			     command=lambda idx=i: toggle_image_selection(idx)
			     )
			image = detection.image
			image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
			image = cv2.resize(image, (100, 100))
			img_tk = ImageTk.PhotoImage(Image.fromarray(image))
			checkbox.img = img_tk
			checkbox.config(image = img_tk)
			checkbox.grid(row=0, column=i, padx=10, pady=10)
			i+=1

		#add buttons to action frame
		save_btn = tk.Button(action_frame, text="Save", command=lambda: save_montage())
		save_btn.pack(side=tk.LEFT)


# Create and run the MontageMakerApp instance
app = MontageMakerApp()
app.run()
