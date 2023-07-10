import cv2
import mediapipe as mp


left_eye_outline = [263,249,390,373,374,381,382,362,398,384,385,386,387,388,466]
right_eye_outline = [133,155,154,153,145,144,163,33,246,161,160,159,158,157,173]
lips_outline= [61,185,40,39,37,0,267,269,270,409,291,375,321,405,314,17,84,181,91,146]
face_outline = [138,135,169,170,140,171,175,396,369,395,394,364,367,435,401,366,447,264,368,301,298,333,299,337,151,108,69,104,68,71,139]
head_outline = [338,10,109,67,103,54,21,162,127,234,93,132,58,172,136,150,149,176,148,152,377,400,378,379,365,397,288,361,323,454,356,389,251,284,332,297]
#Face Mesh

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh()

class detector:

	def detect(self,image_path):

		image = cv2.imread(image_path)
		height, width, _ = image.shape
		rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

		#Facial landmarks
		result = face_mesh.process(image)


		for facial_landmarks in result.multi_face_landmarks:
			# for i in range(0, 468):

    # eye_top = int(landmarks[263].y * image.shape[0])
    # eye_left = int(landmarks[362].x * image.shape[1])
    # eye_bottom = int(landmarks[374].y * image.shape[0])
    # eye_right = int(landmarks[263].x * image.shape[1])
    # right_eye = image[eye_top:eye_bottom, eye_left:eye_right]
			# eye_cordinates = left_eye_index;
			# eye_cordinates.
			for i in head_outline:

				pt1 = facial_landmarks.landmark[i]
				x = int(pt1.x * width)
				y = int(pt1.y * height)

				cv2.circle(image, (x,y), 2, (100,100,0), -1)
				#cv2.putText(image, str(i), (x,y), 0,1,(0,0,0))



		cv2.imshow("Face Mesh detection", image)
		cv2.waitKey(0),