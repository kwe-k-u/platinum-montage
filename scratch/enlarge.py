import numpy as np
import cv2


arr = np.zeros([10,50])

for row in arr:
	row[10] = 255
resize = cv2.resize(arr,(100,500))
for i in range(len(resize[10])):
	points = resize[10][i]
	if points != 0:
		break
print(arr.shape[0]/10,resize.shape[0]/i,arr.shape[0]/10 == resize.shape[0]/10)

#cv2.imshow("ar",arr)
#cv2.imshow("resize",resize)
#cv2.waitKey(0)
