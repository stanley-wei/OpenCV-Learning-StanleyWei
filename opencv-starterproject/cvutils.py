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

def median_blur(image, kernel, passes = 1, showPasses = False):
    blurred = image.copy()
    for i in range(passes):
        blurred = cv2.medianBlur(blurred, kernel)
        if showPasses is True:
            cv2.imshow("Median Pass #" + str(i + 1), blurred)
    return blurred

def median_blur_image_copy(image, kernel, num_passes = 1, show_passes = False):
    image_copy = image.copy()
    image_copy = median_blur(image_copy, kernel, passes = num_passes, showPasses = show_passes)
    return image_copy
