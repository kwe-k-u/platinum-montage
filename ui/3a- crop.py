import tkinter as tk
from tkinter import filedialog
import cv2
import numpy as np
from PIL import Image, ImageTk

class ImageCropperApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Image Cropper")
        self.image_path = None
        self.image = None
        self.crop_rect = None
        self.crop_start = None
        self.crop_mode = "custom"  # or "16:9"

        # Load image button
        self.load_button = tk.Button(self.root, text="Load Image", command=self.load_image)
        self.load_button.pack(pady=10)

        # Image label to display the loaded image
        self.image_label = tk.Label(self.root)
        self.image_label.pack()

        # Toggle button to switch between custom and 16:9 modes
        self.toggle_button = tk.Button(self.root, text="16:9 Mode", command=self.toggle_mode)
        self.toggle_button.pack()

        # Confirm button to crop the image
        self.confirm_button = tk.Button(self.root, text="Confirm", command=self.crop_image)
        self.confirm_button.pack(pady=10)
        self.confirm_button.config(state=tk.DISABLED)  # Disable until image loaded

        # Bind mouse events to the image label
        self.image_label.bind("<ButtonPress-1>", self.on_mouse_press)
        self.image_label.bind("<B1-Motion>", self.on_mouse_drag)
        self.image_label.bind("<ButtonRelease-1>", self.on_mouse_release)

        self.root.mainloop()

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.png;*.jpeg")])
        if file_path:
            self.image_path = file_path
            self.image = cv2.imread(self.image_path)
            self.show_image()

    def show_image(self):
        # Resize the image to fit the label
        h, w, _ = self.image.shape
        max_height = 600
        max_width = 800
        if h > max_height or w > max_width:
            scale = min(max_height / h, max_width / w)
            self.image = cv2.resize(self.image, (int(w * scale), int(h * scale)))

        # Convert the image to RGB and display in the label
        image_rgb = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        image_tk = ImageTk.PhotoImage(Image.fromarray(image_rgb))
        self.image_label.config(image=image_tk)
        self.image_label.image = image_tk
        self.confirm_button.config(state=tk.NORMAL)

    def toggle_mode(self):
        if self.crop_mode == "custom":
            self.crop_mode = "16:9"
            self.toggle_button.config(text="Custom Mode")
        else:
            self.crop_mode = "custom"
            self.toggle_button.config(text="16:9 Mode")

        self.show_image_with_cropping_frame()

    def on_mouse_press(self, event):
        self.crop_start = (event.x, event.y)

    def on_mouse_drag(self, event):
        if self.crop_start:
            self.crop_rect = (self.crop_start[0], self.crop_start[1], event.x, event.y)
            self.show_image_with_cropping_frame()

    def on_mouse_release(self, event):
        self.crop_start = None

    def show_image_with_cropping_frame(self):
        image_with_frame = self.image.copy()

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

    def crop_image(self):
        if self.crop_rect:
            x1, y1, x2, y2 = self.crop_rect
            cropped_image = self.image[y1:y2, x1:x2]
            cropped_image_rgb = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB)
            cropped_image_pil = Image.fromarray(cropped_image_rgb)

            # Save the cropped image or perform other actions
            cropped_image_pil.show()

# Create and run the ImageCropperApp instance
app = ImageCropperApp()
