import cv2
import math

class detection:


	def get_marked_img(self):
		marked = self.image.copy()
		# show face
		for cord in self.face_detection:
			cv2.circle(marked, cord,1,(100,100,1),1)
		# show eyes
		for cord in self.left_eye_detection + self.right_eye_detection:
			cv2.circle(marked, cord,1,(100,100,1),1)
		# show lips
		for cord in self.lip_detection:
			cv2.circle(marked, cord,1,(100,100,1),1)
		return marked

	def __init__(self, row) -> None:
		self.left_eye_detection = []
		self.right_eye_detection = []
		self.lip_detection = []
		self.face_detection = []
		self.nose_detection = []

		self.file = row[0].value if type(row[0]) != str else row[0]
		self.image = cv2.imread(self.file)
		self.img_height = row[1].value if type(row[1]) != int else row[1]
		self.img_width = row[2].value if type(row[2]) != int else row[2]

		for e in range(0,len(row[3:]),2):
			if type(row[3:][e]) == int:
				value = (row[3:][e],row[3:][e+1])
			else:
				value = (row[3:][e].value,row[3:][e+1].value)

			if (len(self.left_eye_detection) < 15): #left eye cordinates
				self.left_eye_detection.append(value)

			elif (len(self.right_eye_detection) < 15 ):
				self.right_eye_detection.append(value)

			elif (len(self.lip_detection) < 31 ):
				self.lip_detection.append(value)

			elif (len(self.face_detection) < 36 ):
				self.face_detection.append(value)

			elif (len(self.nose_detection) < 22 ):
				self.nose_detection.append(value)




	def __eq__(self, obj: object) -> bool:
		return self.left_eye_detection == obj.left_eye_detection and self.right_eye_detection == obj.right_eye_detection and self.lip_detection == obj.lip_detection


	# Checks if the eyes, nose and lips are within the cordinates of the face
	# If these fail, there's a problem with the detection
	# Also checks to see if the detection of face outline is circular (if no then detection failed).
	# OUTPUTS a tuple[4] with booleans to indicate success. Indexes for detections are provided below
	# 0 -> Successful detection status
	# 1 -> Face detection  status
	# 2 -> eye detection  status
	# 3 -> lip detection  status
	# 4 -> nose detection  status
	def is_valid(self):
		# variables for reference feature points for face
		f_151 = self.face_detection[24]
		f_104 = self.face_detection[27]
		f_71 = self.face_detection[29]
		f_138 = self.face_detection[0]
		f_175 = self.face_detection[6]
		f_170 = self.face_detection[3]
		f_395 = self.face_detection[9]
		f_435 = self.face_detection[13]
		f_264 = self.face_detection[17]
		f_299 = self.face_detection[22]

		# variables for reference feature points for eyes
		le_263 = self.left_eye_detection[0]
		le_386 = self.left_eye_detection[11]
		re_133 = self.right_eye_detection[0]
		re_159 = self.right_eye_detection[11]


		# variables for reference feature points for nose
		# n_141 = self.nose_detection[9]
		# n_437 = self.nose_detection[19]



		# variables for reference feature points for lips
		l_0 = self.lip_detection[0]
		l_291 = self.lip_detection[10]

		# the center cordinates for the lips, left& right eyes
		left_eye_center = (le_386[0],le_263[1])
		right_eye_center = (re_159[0],re_133[1])
		lip_center = (l_0[0],l_291[1])
		# nose_center = (n_141[0],n_437[1])

# ==================== sub functions ================================================================
		def is_face_valid():
			return ((f_151[0] > f_104[0] and f_151[0] < f_299[0]) and (f_104[0] > f_71[0] and f_104[0] < f_151[0])
	   		   and (f_71[1] < f_170[1] and f_71[1] > f_104[1]) and (f_170[0] > f_71[0] and f_170[0] < f_175[1])
			   and (f_175[0] < f_395[0]) and (f_264[1] > f_299[1] and f_264[1] < f_395[1])
	   		)

		# Checks major points if their expected positions relative
		# to other points for the feature are true
		def is_left_eye_valid():
			return ((left_eye_center[0]>f_71[0] and left_eye_center[0] < f_264[0]) #horizontal check
			and (left_eye_center[1]> f_299[1] and left_eye_center[1] < f_395[1])) # vertical check

		# Checks major points if their expected positions relative
		# to other points for the feature are true
		def is_right_eye_valid():
			return ( (right_eye_center[0] < f_175[0] and right_eye_center[0] > f_71[0]) # horizontal check
	   		and (right_eye_center[1] > f_104[1] and right_eye_center[1] < f_138[1]) # vertical check
			)

		# Checks major points if their expected positions relative
		# to other points for the feature are true
		def is_lip_valid():
			return ( (lip_center[0]< f_435[0] and lip_center[0] > f_138[0]) #horizontal check
	   		and (lip_center[1] > f_151[1] and lip_center[1] < f_175[1]) #vertical check
			)



		# Checks major points if their expected positions relative
		# to other points for the feature are true
		# def is_nose_valid():
		# 	return ( (nose_center[0] > f_138[0] and nose_center[0] < f_435[0]) #horizontal check
		# 		and (nose_center[1] > f_151[1] and nose_center[1] < f_175[1]) #vertical check
		# 	)




# ====================================================================================
		face = is_face_valid()
		eye = is_left_eye_valid() and is_right_eye_valid()
		lip = is_lip_valid()
		nose = True#is_nose_valid()
		return (face and eye and lip and nose, face, eye, lip, nose)







