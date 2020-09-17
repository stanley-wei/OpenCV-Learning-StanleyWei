from ring_finder import *
import cv2
import time

def main():
    #840x490, 720x420, 576x336
    frameWidth = 576
    frameHeight = 336

    cap = cv2.VideoCapture(4)
    cap.set(3, frameWidth)
    cap.set(4, frameHeight)

    if not cap.isOpened():
        print("Could not open camera")
        exit()
    while True:
        ret, frame = cap.read()
        frame = frame[0:405, 240:640] #cut out most of video to improve framerate
        #frame = frame[0:405, 0:720] #full video frame here
        if not ret:
            break
        start_time = time.time()
        contours, drawn_contours = find_ring(frame, blur_passes = 1, saturation_blur = True, show_images = False)
        drawn_ring_contours, ring_contour, ring_bounding_box = find_bounding_box(frame, contours, draw_box = False, show_images = False)
        # ring_angle = find_ring_angle(ring_bounding_box[2], ring_bounding_box[3])
        # print("Angle: " + str(ring_angle) + " degrees")
        end_time = time.time()
        elapsed_time = end_time - start_time
        print("Time elapsed: " + str(elapsed_time))
        cv2.imshow('frame', drawn_ring_contours)
        # cv2.imshow('frame', frame)
        if cv2.waitKey(1) == 32:
            break

    cap.release()
    cv2.destroyAllWindows()

main()
