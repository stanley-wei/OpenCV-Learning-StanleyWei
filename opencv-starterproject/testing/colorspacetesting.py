from cvutilstesting import *
from matplotlib import pyplot as plt
import numpy as np
import argparse
import mahotas
import cv2

def main():
    args = parseBasicImageArg()
    image = readImageFromArgs(args)
    cv2.imshow("Original", image)

    # blurred = cv2.GaussianBlur(image, (5, 5), 0)

    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    cv2.imshow("to HSV", hsv_image)

    grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imshow("to Grayscale", grayscale)

    (H, S, V) = cv2.split(hsv_image)
    cv2.imshow("H", H)

    to_lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    cv2.imshow("to LAB", to_lab)

    cv2.waitKey(0)

    '''
    Results: HSV was the one that seemed most useful. RGB has issues with
    lighting, grayscale was worse than RGB for detecting the rings, and
    LAB had too many objects that were a similar color.
    '''

main()
