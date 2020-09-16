import numpy as np
import argparse
import imutils
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to the image")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
cv2.imshow("Original", image)

flipped = imutils.flip(image, True, False)
cv2.imshow("Flipped Horizontally", flipped)

flipped = imutils.flip(image, False, True)
cv2.imshow("Flipped Vertically", flipped)

flipped = imutils.flip(image, True, True)
cv2.imshow("Flipped Horizontally and Vertically", flipped)

cv2.waitKey(0)
