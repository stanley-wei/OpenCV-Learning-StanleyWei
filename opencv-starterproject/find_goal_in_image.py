from goal_finder import *
import cv2
import cvutils
import mathutils
import math

def main():
    frame = cvutils.get_image(show_image = True)
    new_frame = cvutils.median_blur(frame, 15, 5)
    # cv2.imshow("image", frame)
    hsv_image = cv2.cvtColor(new_frame, cv2.COLOR_BGR2HSV)
    (H, S, V) = cv2.split(hsv_image)

    hue_copy = H.copy()
    hue_copy = H.copy()
    hue_copy[hue_copy < 100] = 0
    hue_copy[hue_copy > 130] = 0
    saturation_copy = S.copy()
    saturation_copy[S < 120] = 0
    saturation_copy[S > 200] = 0
    mask = cv2.bitwise_and(hue_copy, saturation_copy)
    # cv2.imshow("mask", mask)
    finalimage = cvutils.apply_mask(new_frame, mask, True)

    with_edges, contours = cvutils.find_edges(finalimage)

    if len(contours) > 2:
        center1, radius1 = cv2.minEnclosingCircle(contours[0])
        center2, radius2 = cv2.minEnclosingCircle(contours[1])
        centers = [center1, center2]
        radii = [radius1, radius2]
        for i in range(2, len(contours)):
            contour = contours[i]
            center, radius = cv2.minEnclosingCircle(contour)
            if radius >= radii[0]:
                if mathutils.center_in_circle(centers[0], center, radii[0]) == False:
                    radii[1] = radii[0]
                    centers[1] = centers[0]
                centers[0] = center
                radii[0] = radius
            elif radius >= radii[1]:
                radii[1] = radius
                centers[1] = center
        for i in range(2):
            center = centers[i]
            radius = radii[i]
            print(str(center) + " " + str(radius))
            cv2.circle(frame, (int(center[0]), int(center[1])), int(radius), 255, 3)
            area = math.pi * radius**2
            area = area * 4 / math.pi
            multi = (area / (1.375**2 + 11.882**2)) ** 0.5
            print("Area of Box" + str(i) + ": " + str(area))
            print("Multi of Box" + str(i) + ": " + str(multi))
    new_final = cvutils.draw_contours(frame, contours)

    cv2.imshow("finalimage", new_final)
    cv2.waitKey(0)
main()
