import cv2
class detection:


	def __init__(self, row) -> None:
		self.left_eye_detection = []
		self.right_eye_detection = []
		self.lip_detection = []
		self.face_detection = []
		self.nose_detection = []

		self.file = row[0].value
		self.image = cv2.imread(self.file)
		self.img_height = row[1].value
		self.img_width = row[2].value

		for e in range(0,len(row[3:]),2):
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
		return self.left_eye_detection == obj.left_eye_detection and self.right_eye_detection == obj.right_eye_detection and self.lip_detection == __value.lip_detection