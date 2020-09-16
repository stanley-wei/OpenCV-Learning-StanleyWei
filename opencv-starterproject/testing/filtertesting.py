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

    (H, S, V) = cv2.split(hsv_image)
    cv2.imshow("H", H)

    blurred = cv2.GaussianBlur(H, (5, 5), 0)
    cv2.imshow("Gaussian", blurred)

    blurred = cv2.bilateralFilter(H, 7, 31, 31)
    cv2.imshow("Bilateral", blurred)

    blurred = cv2.medianBlur(H, 5)
    cv2.imshow("Median", blurred)

    cv2.waitKey(0)

    '''
    Test results (in terms of visibility of ring through hue + edges): Median blur, followed by
    unblurred, followed by Gaussian blur, closely followed by the bilateral
    filter had the clearest edges.
    '''

    '''
    Note: Tested four filter types on the actual image itself by applying them
    to the hue channel of the (HSV) image and seeing edge quality + noise level
    when I isolated the H value of the ring.

    Results: Median blur > Gaussian blur > bilateral filter > no blur

    Settings:
        No blur
        Gaussian blur (7, 7)
        Median blur (9)
        Bilateral filter (7, 40, 40)
            - 7 appears to be the ideal 1st parameter
            - 45 > x > 30 is the range for the 2nd and 3rd parameters.
    '''

main()
