from goal_finder import *
import cv2
import cvutils
import mathutils

def main():
    image = cvutils.get_image(show_image = True)
    image = cvutils.median_blur(image, 15, 3)
    # cv2.imshow("image", image)
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    (H, S, V) = cv2.split(hsv_image)
    hue_copy_1 = H.copy()
    hue_copy_2 = H.copy()
    hue_copy_1[hue_copy_1 > 225] = 0
    hue_copy_1[hue_copy_1 > 0] = 255
    hue_copy_2[hue_copy_2 < 160] = 0
    hue_copy_2[hue_copy_2 > 0] = 255
    mask = cv2.bitwise_and(hue_copy_1, hue_copy_2)
    saturation_copy = S.copy()
    saturation_copy[S < 75] = 0
    mask = cv2.bitwise_and(mask, saturation_copy)
    cv2.imshow("mask", mask)
    finalimage = cvutils.apply_mask(image, mask, True)
    cv2.imshow("finalimage", finalimage)

    cv2.waitKey(0)
main()
