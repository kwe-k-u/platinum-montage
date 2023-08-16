import os
import sys
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import cv2

parent = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parent)
from functions import *
from stats_gen import *
from manipulate import *
from detection_class import detection

class MontageMakerApp:
	def __init__(self):
		self.select_folder_window(False)
		self.detection_model = detector()

	#window 1
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
		checks = []

		#allows the user to add and remove images from the list of images to be used
		def select_all_images():
			if len(self.selected_images) == len(image_files):
				self.selected_images = image_files
				#set all check values to true
				for i in range(len(checks)):
					checks[i].set(True)
			else:
				self.selected_images = []
				#set all check values to false
				for i in range(len(checks)):
					checks[i].set(False)

		#allows the use to add and remove images from the list of images to be used
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
		#create a list of tk booleans for each checkbox the size of image_file
		for i in range(len(image_files)):
			image_file = image_files[i]
			# Read the image using cv2
			img = cv2.imread(image_file)
			# Convert the image from BGR to RGB
			img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
			# Resize the image to a smaller size (optional)
			# img = cv2.resize(img, (200, 200))
			img = resize_image(img,200)

			# Convert the image to Tkinter-compatible format
			# img = Image.fromarray(img)
			# img_tk = ImageTk.PhotoImage(img)
			img_tk = create_tk_image(img)

			checks.append(tk.BooleanVar())
			checkbox = tk.Checkbutton(self.root,variable=checks[i],
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

		select_all_button = tk.Button(self.root, text="Select All images", command= select_all_images)
		select_all_button.grid(row=(len(image_files) // 4) + 3, column=1, columnspan=2)

		# Process all images and skip to montage arrangement
		detect_face_button = tk.Button(self.root, text="Detect Face", command=self.skip_to_montage)
		# detect_face_button = tk.Button(self.root, text="Detect Face", command=self.detection_window)
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

		#rotates the image and centers the face in the frame
		def process_image():
			#don't proess images that failed the detection
			if self.detection_list[index] is not None:

				#rotate image to straighten face
				selected = self.detection_list[index]
				_, _, angle = find_eye_angle(selected.left_eye_detection,selected.right_eye_detection)


				processed_img = rotate(selected.image,angle)


				temp_detection = self.detection_model.gen_mesh(selected)
				selected.image = processed_img

				self.detection_list[index] = temp_detection
				selected = self.detection_list[index]

				self.detection_list[index].image = processed_img



			self.detection_window(index)

		def toggle_marks():
			self.show_marks = not self.show_marks
			self.detection_window(index)

		def crop_16_9():
			if self.detection_list[index] == None:
				self.window_crop(self.selected_images[index])
			else:
				self.window_crop(self.detection_list[index])

		def reset_image():
			if self.detection_list[index] is not None:
				report = generate_report([self.detection_list[index].file])
				self.detection_list[index] = detection(report[0])
			else:
				self.detection_list[index] = cv2.imread(self.selected_images[index])

			self.show_marks = True
			self.detection_window(index)


		# def ai_crop():
		# 	selected = self.detection_list[index]
		# 	cropped = crop_img(selected.file)
		# 	self.show_marks = False

		# 	self.detection_list[index].image = cropped

		# 	self.detection_window(index)



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
				try:
					detection_row = generate_report([f])
					detect = detection(detection_row[0])
					self.detection_list.append(detect)
				except:
					self.detection_list.append(None)


		# Create a grid of images in the first frame
		row = 0
		col = 0
		for i in range(len(self.detection_list)):

			#PERFORMING DETECTIONS
			# detector = detector()

			if self.detection_list[i] == None:
				img = cv2.imread(self.selected_images[i])
			else:
				img =  self.detection_list[i].get_marked_img()
			# detector.gen_mesh(image_file)
			# Read the image using cv2
			# img = cv2.imread(image_file)
			# Convert the image from BGR to RGB


			img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
			#resize image and maintain aspect ratio
			img = resize_image(img)


			# Convert the image to Tkinter-compatible format
			img_tk = create_tk_image(img)
			# img = Image.fromarray(img)
			# img_tk = ImageTk.PhotoImage(img)


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

		if detect == None:
			img = cv2.imread(self.selected_images[index])
		elif (self.show_marks):
			img = detect.get_marked_img()
		else:
			img = detect.image

		img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
		img = resize_image(img,750)
		# img = Image.fromarray(img)
		# img_tk = ImageTk.PhotoImage(img)
		img_tk = create_tk_image(img)
		image_label = tk.Label(middle_frame, image=img_tk)
		# image_label.image = img_tk
		image_label.pack()

		#Only show AI functionality if a face is detected
		if detect != None:
			# Detection buttons in the third frame
			face_button = tk.Button(third_frame, text="AI process", command=process_image)
			face_button.pack(pady=5)

		# left_eye_button = tk.Button(third_frame, text="AI Crop", command=ai_crop)
		# left_eye_button.pack(pady=5)

		left_eye_button = tk.Button(third_frame, text="Manual Crop", command=crop_16_9)
		left_eye_button.pack(pady=5)


		reset_button = tk.Button(middle_frame, text="Reset image", command=reset_image)
		reset_button.pack(pady=5)


		show_mark_button = tk.Button(third_frame, text="Toggle marking", command=lambda: toggle_marks() )
		show_mark_button.pack(pady=5)

		show_montage_button = tk.Button(third_frame, text="Create montage", command=self.create_montage_img)
		show_montage_button.pack(pady=5)


		self.root.mainloop()




	# Window 4
	def window_crop(self,detection):

		def show_image():
			#if a string is provided(detection failed), read the file
			if type(detection) == type(""):
				im = cv2.imread(detection)
			else:
				im = detection.image

			# Resize the image to fit the label
			im = resize_image(im, 750)
				# scale = min(max_height / h, max_width / w)
				# self.image = cv2.resize(im, (int(w * scale), int(h * scale)))

			image_rgb = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
			image_tk = create_tk_image(image_rgb)
			# image_tk = ImageTk.PhotoImage(Image.fromarray(image_rgb))
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
			if type(detection) is type(""):
				image_with_frame = cv2.imread(detection)
			else:
				image_with_frame = detection.image.copy()
				image_with_frame = resize_image(image_with_frame, 750)

			if self.crop_mode == "16:9":
				h = image_with_frame.shape[0]
				aspect_ratio =  9/ 16
				crop_width = int(h * aspect_ratio)

				# Center the cropping frame around the click (if in 16:9 mode)
				if self.crop_rect and self.crop_start:
					cx = (self.crop_rect[0] + self.crop_rect[2]) // 2
					cy = (self.crop_rect[1] + self.crop_rect[3]) // 2
					self.crop_rect = (cx - crop_width // 2, cy - h // 2, cx + crop_width // 2, cy + h // 2)

				dark_tint = np.zeros(image_with_frame.shape, dtype=np.uint8)
				dark_tint.fill(10)  # Darken the tint

				# Apply the dark tint to the areas outside the cropping frame
				image_with_frame = np.where(dark_tint > image_with_frame, dark_tint, image_with_frame)

			if self.crop_rect:
				cv2.rectangle(image_with_frame, (self.crop_rect[0], self.crop_rect[1]),
							(self.crop_rect[2], self.crop_rect[3]), (255, 0, 0), 2)

			image_rgb = cv2.cvtColor(image_with_frame, cv2.COLOR_BGR2RGB)
			# image_tk = ImageTk.PhotoImage(Image.fromarray(image_rgb))
			image_tk = create_tk_image(image_rgb)
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
		self.toggle_button = tk.Button(self.root, text="Switch to Custom Mode", command=toggle_mode)
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


	# skip to montage window
	def skip_to_montage(self):
		#show a loading page
		self.root.destroy()
		self.root = tk.Tk()
		self.root.title("Loading")
			# Create a label to display the loading text
		loading_label = tk.Label(self.root, text="Processing Images", font=("Helvetica", 16))
		loading_label.pack(pady=20)

		# Create a loading icon using the ttk.Progressbar widget
		loading_icon = ttk.Progressbar(self.root, mode="indeterminate")
		loading_icon.pack(pady=10)
		loading_icon.start()
		# self.root.mainloop()

		for i in range(len(self.selected_images)):
			# try:
			report = generate_report([self.selected_images[i]])[0]
			detect = detection(report)
			_,_,angle = find_eye_angle(detect.left_eye_detection,detect.right_eye_detection)
			# print(angle)
			print(detect)
			proc_img = rotate(detect.image,angle)
			detect = self.detection_model.gen_mesh(detect)
			detect.image = proc_img
			self.detection_list.append(detect)
			# except:
				# print("error caught")
				# log error

				# self.detection_list.append(None)

		self.create_montage_img()


	# Window 5 - create and save montage image
	def create_montage_img(self):
		montage_order = []

		def update_montage_image():
			#if montage_order is empty show a black image
			if len(montage_order) == 0:
				self.montage = np.zeros((400, 400, 3), np.uint8)
				# img = Image.fromarray(self.montage)
				# img_tk = ImageTk.PhotoImage(img)
				img_tk = create_tk_image(self.montage)
				self.montage_image_label.config(image=img_tk)
				self.montage_image_label.image = img_tk

			#get images from self.detection_list by indexes in montage_order
			#create one image with all the images side by side
			else:
				images = []
				for i in montage_order:
					if self.detection_list[i] is None:
						mon_image = cv2.imread(self.selected_images[i])
					else:
						mon_image = self.detection_list[i].image

					mon_image = cv2.cvtColor(mon_image, cv2.COLOR_BGR2RGB)
					# mon_image = cv2.resize(mon_image, (250, 250))
					mon_image = resize_image(mon_image,250)
					images.append(mon_image)


				#concatenate images
				self.montage = np.concatenate(images, axis=1)

				# montage = Image.fromarray(self.montage)
				# montage_tk = ImageTk.PhotoImage(montage)
				montage_tk = create_tk_image(self.montage)
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
			for i in range(len(self.detection_list)):
				#change name from img.ext to imgA.ext
				if self.detection_list[i] is None:
					parts = self.selected_images[i].split(".")
				else:
					parts = self.detection_list[i].file.split(".")

				new_name = ".".join(parts[:-1]) + "a." + parts[-1]
				if self.detection_list[i] is None:
					sav_im = cv2.imread(self.selected_images[i])
				else:
					sav_im = self.detection_list[i].image

				print("saving ",new_name)
				cv2.imwrite(new_name, sav_im)

			#save montage to file
			montage = cv2.cvtColor(self.montage, cv2.COLOR_BGR2RGB)
			print("saving montage: ",".".join(parts[:-1])+"montage.jpg")
			cv2.imwrite(".".join(parts[:-1])+"-montage.jpg", montage)



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
		# img = Image.fromarray(img)
		# img_tk = ImageTk.PhotoImage(img)
		img_tk = create_tk_image(img)
		self.montage_image_label.config(image=img_tk)
		self.montage_image_label.image = img_tk
		self.montage_image_label.pack()

		i = 0
		for detect in self.detection_list:
			checkbox = tk.Checkbutton(botom_frame, variable=tk.BooleanVar(),
			     command=lambda idx=i: toggle_image_selection(idx)
			     )
			if detect is None:
				image = cv2.imread(self.selected_images[i])
			else:
				image = detect.image

			image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
			image = resize_image(image,300)
			# image = cv2.resize(image, (100, 100))
			# img_tk = ImageTk.PhotoImage(Image.fromarray(image))
			img_tk = create_tk_image(image)
			checkbox.img = img_tk
			checkbox.config(image = img_tk)
			checkbox.grid(row=0, column=i, padx=10, pady=10)
			i+=1

		#add buttons to action frame
		save_btn = tk.Button(action_frame, text="Save", command=lambda: save_montage())
		save_btn.pack(side=tk.LEFT)


# Create and run the MontageMakerApp instance
if __name__ == "__main__":
	app = MontageMakerApp()
	app.run()
