import cv2
import mediapipe as mp


left_eye_outline = [263,249,390,373,374,381,382,362,398,384,385,386,387,388,466]
right_eye_outline = [133,155,154,153,145,144,163,33,246,161,160,159,158,157,173]
lips_outline= [61,185,40,39,37,0,267,269,270,409,291,375,321,405,314,17,84,181,91,146]
face_outline = [138,135,169,170,140,171,175,396,369,395,394,364,367,435,401,366,447,264,368,301,298,333,299,337,151,108,69,104,68,71,139]
# head_outline = [338,10,109,67,103,54,21,162,127,234,93,132,58,172,136,150,149,176,148,152,377,400,378,379,365,397,288,361,323,454,356,389,251,284,332,297]
nose_outline = [114,217,198,131,115,218,79,20,242,141,94,370,462,250,309,438,344,360,420,437,343,357]

class detector:
	image = None
	face_mesh = None
	num_detections = 0

	# converts the image path into an image object and obtains the face mesh for the image
	def gen_mesh(self,image_path):
		mp_face_mesh = mp.solutions.face_mesh
		face_mesh = mp_face_mesh.FaceMesh()

		self.image = cv2.imread(image_path)
		# rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

		#Facial landmarks
		self.face_mesh = face_mesh.process(self.image)



	# Shows the selected landmarks with red dots
	def show(self,landmarks):
		image = self.image.copy()

		for cord in landmarks:
				cv2.circle(image, cord, 2, (100,100,0), 1)

		cv2.imshow("Face Mesh detection", image)
		cv2.waitKey(0)



	# converts the landmark index to the pixel cordinate in the image
	def mark(self,cordinate_index):
		cordinates = []
		self.num_detections = self.num_detections + 1
		# print("Detection count " + str(self.num_detections))

		height, width, _ = self.image.shape

		for facial_landmarks in self.face_mesh.multi_face_landmarks:
			for i in cordinate_index:

				pt1 = facial_landmarks.landmark[i]
				x = int(pt1.x * width)
				y = int(pt1.y * height)
				#cv2.putText(image, str(i), (x,y), 0,1,(0,0,0))
				cordinates.append((x,y))

		return cordinates

	# returns the pixel cordinates for the eyes in the image
	def detect_left_eye(self):
		return self.mark(left_eye_outline)

	# returns the pixel cordinates for the eyes in the image
	def detect_right_eye(self):
		return self.mark(right_eye_outline)


	# returns the pixel cordinates for the eyes in the image
	def detect_face(self):
		return self.mark(face_outline)

	def detect_lips(self):
		return self.mark(lips_outline)


	def detect_nose(self):
		return self.mark(nose_outline)

