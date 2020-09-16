import numpy as np
import cv2

def translate(image, x, y):
  M = np.float32([[1, 0, x], [0, 1, y]])
  shifted = cv2.warpAffine(image, M, (image.shape[1], image.shape[0]))

  return shifted

def rotate(image, angle, center = None, scale = 1.0):
    (h, w) = image.shape[:2]

    if center is None:
        center = (w // 2, h // 2)

    M = cv2.getRotationMatrix2D(center, angle, scale)
    rotated = cv2.warpAffine(image, M, (w, h))
    return rotated

def resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image

    if height is None:
        r = width / float(w)
        dim = (width, int(h * r))

    else:
        r = height / float(h)
        dim = ((int(w * r)), height)

    resized = cv2.resize(image, dim, inter)
    return resized

def flip(image, horizontal = False, vertical = False):
    if horizontal is False and vertical is False:
        return image

    if horizontal is False:
        flip_code = 0

    elif vertical is False:
        flip_code = 1

    else:
        flip_code = -1

    flipped = cv2.flip(image, flip_code)
    return flipped

def crop(image, x_area = None, y_area = None):
    if x_area is None and y_area is None:
        return image

    if x_area is None:
        x_area = (0, image.shape[1])
    elif y_area is None:
        y_area = (0, image.shape[0])

    cropped = image[y_area[0]:y_area[1], x_area[0]:x_area[1]]
    return cropped
