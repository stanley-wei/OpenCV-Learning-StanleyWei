from cvutils import *
from matplotlib import pyplot as plt
import numpy as np
import argparse
import mahotas
import cv2

def main():
    args = parseBasicImageArg()
    image = readImageFromArgs(args)
    cv2.imshow("Original", image)

    #Tried applying a blur to the original image here to improve accuracy, but it doesn't significantly affect the final result.
    image_copy = image.copy()
    for i in range(3):
        image_copy = cv2.medianBlur(image_copy, 9)
        cv2.imshow("Median Blur, pass #" + str(i+2), image_copy)

    hsv_image = cv2.cvtColor(image_copy, cv2.COLOR_BGR2HSV)
    cv2.imshow("to HSV", hsv_image)

    (H, S, V) = cv2.split(hsv_image)
    cv2.imshow("H", H)

    #I found that applying blurs multiple times often was much better for reducing noise than just running it once.
    blurred_H = H.copy()
    for i in range(3):
        blurred_H = cv2.medianBlur(blurred_H, 9)
        cv2.imshow("Median Blur, pass #" + str(i+2), blurred_H)

    blurred_S = S.copy()
    for i in range(3):
        blurred_S = cv2.medianBlur(blurred_S, 9)
        cv2.imshow("Median Blur, pass #" + str(i+2), blurred_S)

    white_background = blurred_H.copy()
    white_background[white_background > 12] = 0
    # white_background[white_background < 10] = 0
    cv2.imshow("Hue Isolation", white_background)

    #I still had too much noise even with the hue mask, so I added a saturation mask to help cut it down further.
    saturation_mask = blurred_S.copy()
    saturation_mask[saturation_mask > 235] = 0
    saturation_mask[saturation_mask < 165] = 0
    cv2.imshow("Saturation Isolation", saturation_mask)

    #By applying the saturation mask to the hue mask, I can eliminate many of the incorrect points.
    mask = white_background.copy()
    mask[mask > 20] = 0
    cv2.imshow("mask", mask)
    mask = cv2.bitwise_and(mask, mask, mask = saturation_mask)
    cv2.imshow("masked mask", mask)
    image_with_mask = cv2.bitwise_and(image, image, mask = mask)
    cv2.imshow("Image with mask", image_with_mask)

    canny = cv2.Canny(image_with_mask, 10, 250)
    cv2.imshow("Canny", canny)

    (contours, _) = cv2.findContours(canny.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    drawn_contours = image.copy()
    cv2.drawContours(drawn_contours, contours, -1, (0, 255, 0), 2)
    cv2.imshow("Contours", drawn_contours)

    #Here I assume the largest contour is the ring itself and try to find it by comparing bounding box sizes.
    largest_contour = contours[0]
    bounding_box = (0, 0, 0, 0)
    bounding_box_area = 0
    for (i, c) in enumerate(contours):
        (x, y, w, h) = cv2.boundingRect(c)
        area = w * h
        if area > bounding_box_area:
            bounding_box_area = area
            largest_contour = c
            bounding_box = (x, y, w, h)

    drawn_contours = image.copy()
    cv2.drawContours(drawn_contours, largest_contour, -1, (0, 255, 0), 2)
    cv2.rectangle(drawn_contours, (bounding_box[0], bounding_box[1]), (bounding_box[0] + bounding_box[2], bounding_box[1] + bounding_box[3]), (0, 0, 255), 2)
    cv2.imshow("Contours", drawn_contours)

    cv2.waitKey(0)

main()
