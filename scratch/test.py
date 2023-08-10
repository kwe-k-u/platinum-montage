import cv2
import numpy as np
import os

def create_montage(files, faces):
    # Concatenate images horizontally to create a montage
    im_list = []

    for  i in range(len(files)):
        im = cv2.imread(files[i])
        # create np array of zeros with the same shape as the image
        im = np.zeros(im.shape, np.uint8)
        if im.shape[0] > 800:
            im = cv2.resize(im, (int(im.shape[1] * 800 / im.shape[0]), 800))

        
        # cv2.circle(im, faces[0][0], 30, (0, 255, 255), 1)
        for point in faces[i]:
            cv2.circle(im, point, 1, (0, 255, 0), 1)
        im_list.append(im)

    montage_image = np.concatenate(im_list, axis=1)

    height, width = montage_image.shape[:2]
    nw = 1200
    nh = int(height * (nw / width))

    cv2.imshow("montage", cv2.resize(montage_image, (nw, nh)))
    cv2.waitKey(0)
    cv2.destroyAllWindows()



def detect_faces(image_path):
    # Load the image using OpenCV
    image = cv2.imread(image_path)

    # Reduce the image size to shorter than height 800 while maintaining aspect ratio
    height, width = image.shape[:2]
    if height > 800:
        image = cv2.resize(image, (int(width * 800 / height), 800))

    # Convert the image to grayscale for edge detection
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Use Canny edge detection to enhance facial features
    # Add Gaussian blur for better results
    gray_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
    edges = cv2.Canny(gray_image, 70, 150)
    # contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


    outline_cordinates = []
    #for each height in the image:
    height, width = edges.shape[0], edges.shape[1]
    for h in range(height):
        first = None
        last = None
        for w in range(width):
            if edges[h,w] > 0:
                if first is None:
                    first = (w,h)

                # elif last is None:
                last = (w,h)
                # outline_cordinates.append((w,h))
        if first is not None:
            outline_cordinates.append(first)
        if last is not None:
            outline_cordinates.append(last)

    return outline_cordinates



if __name__ == "__main__":
    folder_path = "C:\\Users\\KWAKU\\Desktop\\Platinum Dental\\Montage maker\\pictures"
    faces = []
    files = []
    for filename in os.listdir(folder_path):
        image_extensions = ['.jpg', '.jpeg', '.png']
        _, extension = os.path.splitext(filename)

        if extension.lower() in image_extensions:
            path = os.path.join(folder_path, filename)
            files.append(path)
            face = detect_faces(path)

            faces.append(face)
            print("added image")

    print("show montage")
    create_montage(files,faces)
