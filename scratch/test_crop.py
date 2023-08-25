import cv2
import numpy as np
from random import randint
import math

#create  black images of different sizes
# images = [np.zeros((randint(900,150),randint(900,150),3),dtype=np.uint8) for i in range(5)]
images = [ np.zeros((91,97),dtype=np.uint8),
          np.zeros((85,95),dtype=np.uint8),
          np.zeros((100,90),dtype=np.uint8)
          ]

for image in images:
    cv2.circle(image,(image.shape[1]//2,image.shape[0]//2),10,(255,0,0))

# find the shortest image
short_y = math.inf
for image in images:
    if image.shape[0] < short_y:
        short_y = image.shape[0]

for index in range(len(images)):
    image = images[index]
    if image.shape[0] != short_y:
        yd = image.shape[0] - short_y

        images[index] = images[index] [: -yd] [:]

# concatenate images
montage = np.concatenate([x for x in images],axis=1)
# cv2.line(montage,(0,montage.shape[1]//2),(montage.shape[0],montage.shape[1]//2),(255,0,0))
# cv2.line(montage,(0,50),(montage.shape[1],50),(255,0,0))
# montage = montage[50:][:]
cv2.imshow("montage", montage)
cv2.waitKey(0)

# save image
# cv2.imwrite("testimg1.jpg",montage)