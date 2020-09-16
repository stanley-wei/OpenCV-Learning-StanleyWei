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

    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    cv2.imshow("to HSV", hsv_image)

    (H, S, V) = cv2.split(hsv_image)
    cv2.imshow("S", S)

    blurred = S.copy()
    for i in range(3):
        blurred = cv2.medianBlur(blurred, 9)
        cv2.imshow("Median Blur, pass #" + str(i+2), blurred)

    saturation_mask = blurred.copy()
    saturation_mask[saturation_mask > 240] = 0
    saturation_mask[saturation_mask < 176] = 0
    cv2.imshow("Saturation Isolation", saturation_mask)

    # white_background = blurred.copy()
    # white_background[white_background > 11] = 255
    # white_background[white_background < 10] = 255
    # cv2.imshow("Isolation", white_background)
    #
    # mask = white_background.copy()
    # mask[mask > 20] = 0
    # rgb_mask = oneToThreeChannels(mask)
    # image_with_mask = cv2.bitwise_and(image, image, mask = mask)
    # cv2.imshow("Image with mask", image_with_mask)

    cv2.waitKey(0)

main()
