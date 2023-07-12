

class detection:


	def __init__(self, row) -> None:
		self.left_eye_detection = []
		self.right_eye_detection = []
		self.lip_detection = []
		self.face_detection = []
		self.nose_detection = []

		self.file = row[0].value
		self.img_height = row[1].value
		self.img_width = row[2].value
		# print("\n")
		# print("new obj",self.left_eye_detection)
		# print("new obj",self.right_eye_detection)
		# print("new obj",self.lip_detection)
		first = None
		for e in range(0,len(row[3:]),2):
			value = (row[3:][e].value,row[3:][e+1].value)
			if(e==0):
				first = value
			# print(value,end=",")

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

		# print(first,self.left_eye_detection[0])



	def __eq__(self, obj: object) -> bool:
		print("self name "+ str(self.img_height),self.file)
		print("self name "+ str(obj.img_height),obj.file)
		return self.file == obj.file
		return self.left_eye_detection == obj.left_eye_detection and self.right_eye_detection == obj.right_eye_detection and self.lip_detection == __value.lip_detection