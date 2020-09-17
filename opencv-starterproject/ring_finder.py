from matplotlib import pyplot as plt
import numpy as np
import argparse
import mahotas
import cv2
import cvutils
import time
import math
import mathutils

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
        sine_plus, sine_minus = mathutils.quadratic_formula(-0.75, 5, c_constant)

        if 1 > sine_plus > -1:
            ring_angle_sine = sine_plus
        else:
            ring_angle_sine = sine_minus

        ring_angle = math.asin(ring_angle_sine)

    ring_angle_degrees = ring_angle * (180.0 / math.pi)
    return ring_angle, ring_angle_degrees

def find_ring(image, blur_passes = 1, saturation_blur = True, show_images = False):
    image_copy = image.copy()
    image_with_mask, processed_image = process_image(image_copy, blur_passes = blur_passes, saturation_blur = saturation_blur, show_images = show_images)

    canny, contours = find_ring_edges(image_with_mask, show_images = show_images)
    drawn_contours = cvutils.draw_contours(image, contours, show_image = show_images)

    return contours, drawn_contours

def find_bounding_box(image, contours, draw_box = True, show_images = False):
    #Here I assume the largest contour is the ring itself and try to find it by comparing bounding box sizes.
    (largest_contour, bounding_box) = cvutils.find_largest_bounding_box(contours)
    (bounding_box_topleft, bounding_box_bottomright) = cvutils.get_rectangle_corners(bounding_box)

    drawn_ring_contours = cvutils.draw_contours(image, largest_contour)
    if draw_box is True:
        cv2.rectangle(drawn_ring_contours, bounding_box_topleft, bounding_box_bottomright, (0, 0, 255), 2)
    if show_images is True:
        cv2.imshow("Contours", drawn_ring_contours)

    return drawn_ring_contours, largest_contour, bounding_box

def process_image(image, blur_passes = 1, saturation_blur = True, show_images = False):
    image_copy = image.copy()

    #Tried applying a blur to the original image here to improve accuracy,
    #but it doesn't significantly affect the final result or time elapsed.
    image_copy = cvutils.median_blur(image, 9, num_passes = blur_passes, show_passes = show_images)

    hsv_image = cv2.cvtColor(image_copy, cv2.COLOR_BGR2HSV)
    if show_images is True:
        cv2.imshow("to HSV", hsv_image)

    (H, S, V) = cv2.split(hsv_image)
    if show_images is True:
        cv2.imshow("H", H)

    # I found that applying blurs multiple times often was much better for reducing noise than just running it once.
    # Note: not using median_blur_image_copy because i prefer this way (it's easier to read)
    blurred_H = H.copy()
    blurred_H = cvutils.median_blur(blurred_H, 9, num_passes = blur_passes, show_passes = show_images)

    blurred_S = S.copy()
    if saturation_blur is True:
        blurred_S = cvutils.median_blur(blurred_S, 9, num_passes = blur_passes, show_passes = show_images)

    # this doesn't serve any major purpose, it's just easier to see the cropped parts on a white background
    white_background = blurred_H.copy()
    white_background[white_background > 12] = 0
    # white_background[white_background < 10] = 0
    if show_images is True:
        cv2.imshow("Hue Isolation", white_background)

    #I still had too much noise even with the hue mask, so I made a saturation mask to help cut it down further.
    saturation_mask = blurred_S.copy()
    saturation_mask[saturation_mask > 235] = 0
    saturation_mask[saturation_mask < 165] = 0
    if show_images is True:
        cv2.imshow("Saturation Isolation", saturation_mask)

    mask = white_background.copy()
    mask = cvutils.simple_threshold(mask, max_val = 20, max_set = 0, show_thresh = show_images)
    if show_images is True:
        cv2.imshow("mask", mask)

    #By applying the saturation mask to the hue mask, I can eliminate many of the incorrect points.
    mask = cvutils.apply_mask(mask, saturation_mask, show_result = show_images)
    image_with_mask = cvutils.apply_mask(image, mask, show_result = show_images)

    return image_with_mask, image_copy

def find_ring_edges(image, show_images = False):
    canny = cv2.Canny(image, 10, 250)
    if show_images is True:
        cv2.imshow("Canny", canny)

    (contours, _) = cv2.findContours(canny.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    return canny, contours
