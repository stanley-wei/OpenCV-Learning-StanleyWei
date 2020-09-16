from cvutils import *
from matplotlib import pyplot as plt
import numpy as np
import argparse
import mahotas
import cv2
import time
import math

def find_ring_angle(width, height):
    if width > height:
        inches_per_pixel = 5.0 / width
        ratio = height/width
    else:
        inches_per_pixel = 5.0 / height
        ratio = width/height

    if 1.05 > ratio > 0.95: # when the ring is perfectly upright
        ring_angle = math.pi/2.0
    elif 0.2 > ratio > 0.1: # when the ring is nearly flat
        ring_angle = 0
    else:
        inches_height = height * inches_per_pixel
        c_constant = 0.75 - inches_height
        sines = quadratic_formula(-0.75, 5, c_constant)

        if 1 > sines[0] > -1:
            ring_angle_sine = sines[0]
        else:
            ring_angle_sine = sines[1]

        ring_angle = math.asin(ring_angle_sine)

    ring_angle_degrees = ring_angle * (180.0 / math.pi)
    return ring_angle, ring_angle_degrees

def quadratic_formula(a, b, c):
    root_expression = math.sqrt((b**2) - (4 * a * c))
    numerator_plus = -b + root_expression
    numerator_minus = -b - root_expression
    denominator = 2 * a

    answer_plus = numerator_plus / denominator
    answer_minus = numerator_minus / denominator

    return[answer_plus, answer_minus]

def main():
    start_timestamp = time.time()

    image = get_image(show_image = True)

    #Tried applying a blur to the original image here to improve accuracy,
    #but it doesn't significantly affect the final result or time elapsed.
    image_copy = median_blur_image_copy(image, 9, num_passes = 3, show_passes = False)

    hsv_image = cv2.cvtColor(image_copy, cv2.COLOR_BGR2HSV)
    cv2.imshow("to HSV", hsv_image)

    (H, S, V) = cv2.split(hsv_image)
    cv2.imshow("H", H)

    # I found that applying blurs multiple times often was much better for reducing noise than just running it once.
    # Note: not using median_blur_image_copy because i prefer this way (it's easier to read)
    blurred_H = H.copy()
    blurred_H = median_blur(blurred_H, 9, passes = 3, showPasses = True)

    blurred_S = S.copy()
    blurred_S = median_blur(blurred_S, 9, passes = 3, showPasses = True)

    # this doesn't serve any major purpose, it's just easier to see the cropped parts on a white background
    white_background = blurred_H.copy()
    white_background[white_background > 12] = 0
    # white_background[white_background < 10] = 0
    cv2.imshow("Hue Isolation", white_background)

    #I still had too much noise even with the hue mask, so I made a saturation mask to help cut it down further.
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

    end_timestamp = time.time()
    time_elapsed = end_timestamp - start_timestamp
    print("Time elapsed: " + str(time_elapsed))

    (ring_angle, ring_angle_degrees) = find_ring_angle(bounding_box[2], bounding_box[3])
    print("Ring angle: " + str(ring_angle_degrees) + " degrees")

    cv2.waitKey(0)

main()
