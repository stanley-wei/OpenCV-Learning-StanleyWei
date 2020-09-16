import numpy as np
import argparse
import imutils
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to the image")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
cv2.imshow("Original", image)

cropped = imutils.crop(image, x_area = (20, 50))
cv2.imshow("Horizontal Crop", cropped)

cropped = imutils.crop(image, y_area = (20, 50))
cv2.imshow("Vertical Crop", cropped)

cropped = imutils.crop(image, x_area = (20, 60), y_area = (20, 60))
cv2.imshow("Crop", cropped)

cv2.waitKey(0)
