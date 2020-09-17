from ring_finder import *
import cv2
import time

def main():
    #840x490, 720x420, 576x336 fit the aspect ratio
    frameWidth = 576
    frameHeight = 336

    #OBS camera port is 4 when the webcam is connected, 2 otherwise
    video_capture = cv2.VideoCapture(2)
    video_capture.set(3, frameWidth)
    video_capture.set(4, frameHeight)

    if not video_capture.isOpened():
        print("Could not open camera")
        exit()

    while True:
        read, frame = video_capture.read()
        frame = frame[0:405, 240:640] #cut out most of video to improve framerate
        #frame = frame[0:405, 0:720] #full video frame here
        if not read:
            print("Camera could not be read")
            break
        start_time = time.time()
        contours, drawn_contours = find_ring(frame, blur_passes = 1, saturation_blur = True, show_images = False)
        drawn_ring_contours, ring_contour, ring_bounding_box = find_bounding_box(frame, contours, draw_box = False, show_images = False)
        # ring_angle = find_ring_angle(ring_bounding_box[2], ring_bounding_box[3])
        # print("Angle: " + str(ring_angle) + " degrees")
        end_time = time.time()
        elapsed_time = end_time - start_time
        # print("Time elapsed: " + str(elapsed_time))
        framerate = 1.0 / elapsed_time
        # if framerate < 10:
        #     cv2.imshow('slowframe', drawn_ring_contours)
        print("FPS: " + str(int(framerate)))
        cv2.imshow('frame', drawn_ring_contours)
        # cv2.imshow('frame', frame)
        if cv2.waitKey(1) == 32:
            break

    video_capture.release()
    cv2.destroyAllWindows()

main()
