import cvutils
import cv2
import time

def main():
    #840x490, 720x420, 576x336 fit the aspect ratio
    frameWidth = 576
    frameHeight = 336

    #OBS camera port is 4 for obs virtualcam when the webcam is connected, 2 otherwise
    #microsoft webcam is 2
    # video_capture = cv2.VideoCapture(int(input("cam#"))) 3
    video_capture = cv2.VideoCapture(1)
    video_capture.set(3, frameWidth)
    video_capture.set(4, frameHeight)

    if not video_capture.isOpened():
        print("Could not open camera")
        exit()

    while True:
        read, frame = video_capture.read()
        frame = cvutils.median_blur(frame, 15, 3)
        # cv2.imshow("image", frame)
        hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        (H, S, V) = cv2.split(hsv_image)
        hue_copy_1 = H.copy()
        hue_copy_2 = H.copy()
        hue_copy_1[hue_copy_1 > 130] = 0
        hue_copy_1[hue_copy_1 > 0] = 255
        hue_copy_2[hue_copy_2 < 110] = 0
        hue_copy_2[hue_copy_2 > 0] = 255
        mask = cv2.bitwise_and(hue_copy_1, hue_copy_2)
        saturation_copy = S.copy()
        saturation_copy[S < 120] = 0
        mask = cv2.bitwise_and(mask, saturation_copy)
        # cv2.imshow("mask", mask)
        finalimage = cvutils.apply_mask(frame, mask, True)
        cv2.imshow("finalimage", finalimage)
        # cv2.imshow('frame', frame)
        if cv2.waitKey(1) == 32:
            break

    video_capture.release()
    cv2.destroyAllWindows()

main()
