from matplotlib import pyplot as plt
import numpy as np
import argparse
import cv2

def parse_basic_image_arg():
    ap = argparse.ArgumentParser()
    ap.add_argument('-i', '--image', required = True, help = "Path to the image")
    args = vars(ap.parse_args())
    return args

def read_image_from_args(args):
    image = cv2.imread(args['image'])
    return image

def get_image(show_image = False):
    args = parse_basic_image_arg()
    image = read_image_from_args(args)

    if show_image is True:
        cv2.imshow("Original", image)

    return image

def one_to_three_channels(original_channel, main_channel = 0):
    zeros = np.zeros(channel.shape[:2], dtype = "uint8")
    three_channels = [zeros, zeros, zeros]
    three_channels[main_channel] = original_channel
    merged_channels = cv2.merge(three_channels)
    return merged_channels

def median_blur(image, kernel, num_passes = 1, show_passes = False):
    blurred = image.copy()
    for i in range(num_passes):
        blurred = cv2.medianBlur(blurred, kernel)
        if show_passes is True:
            cv2.imshow("Median Pass #" + str(i + 1), blurred)
    return blurred

def median_blur_image_copy(image, kernel, num_passes = 1, show_passes = False):
    image_copy = image.copy()
    image_copy = median_blur(image_copy, kernel, passes = num_passes, showPasses = show_passes)
    return image_copy

def find_largest_bounding_box(contours):
    if len(contours) > 0:
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
        return largest_contour, bounding_box
    else:
        return contours, (0, 0, 0, 0)

def apply_mask(image, mask, show_result = False):
    masked_image = cv2.bitwise_and(image, image, mask = mask)
    if show_result is True:
        cv2.imshow("Masked image", masked_image)
    return masked_image

def draw_contours(image, contours, show_image = False):
    image_copy = image.copy()
    drawn_contours = cv2.drawContours(image_copy, contours, -1, (0, 255, 0), 2)
    if show_image is True:
        cv2.imshow("Contours", drawn_contours)
    return drawn_contours

def find_rectangle_corners(x_origin, y_origin, width, height):
    top_left = (x_origin, y_origin)
    bottom_right = (x_origin + width, y_origin + height)
    return top_left, bottom_right

def get_rectangle_corners(rect_tuple):
    x_origin = rect_tuple[0]
    y_origin = rect_tuple[1]
    width = rect_tuple[2]
    height = rect_tuple[3]
    top_left = (x_origin, y_origin)
    bottom_right = (x_origin + width, y_origin + height)
    return top_left, bottom_right

def simple_threshold(image, min_val = -1, max_val = 256, min_set = 0, max_set = 256, show_thresh = False):
    thresh = image.copy()
    thresh[thresh < min_val] = min_set
    thresh[thresh > max_val] = max_set
    if show_thresh is True:
        cv2.imshow("Thresholded Image", thresh)
    return thresh

def find_edges(image, show_images = False):
    canny = cv2.Canny(image, 10, 250)
    if show_images is True:
        cv2.imshow("Canny", canny)

    (contours, _) = cv2.findContours(canny.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    return canny, contours
