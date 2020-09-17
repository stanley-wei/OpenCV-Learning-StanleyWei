from ring_finder import *
from matplotlib import pyplot as plt
import numpy as np
import argparse
import mahotas
import cv2
import cvutils
import time
import math
import mathutils

def main():
    image = cvutils.get_image(show_image = True)

    contours, drawn_contours = find_ring(image, blur_passes = 3, saturation_blur = True, show_images = True)
    drawn_ring_contours, ring_contour, ring_bounding_box = find_bounding_box(image, contours, draw_box = True, show_images = True)

    (ring_angle, ring_angle_degrees) = find_ring_angle(ring_bounding_box[2], ring_bounding_box[3])
    print("Ring angle: " + str(ring_angle_degrees) + " degrees")

    cv2.waitKey(0)

main()
