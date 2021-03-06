from matplotlib import pyplot as plt
import argparse
import cv2

ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required = True, help = "Path to the image")
args = vars(ap.parse_args())

image = cv2.imread(args['image'])
cv2.imshow("Original", image)

chans = cv2.split(image)
colors = ("b", 'g', 'r')
plt.figure()
plt.title("'Flattened' Color Histogram")
plt.xlabel("Bins")
plt.ylabel("# of Pixels")

for (chan, color) in zip(chans, colors):
    hist = cv2.calcHist([chan], [0], None, [256], [0, 256])
    plt.plot(hist, color = color)
    plt.xlim([0, 256])

fig = plt.figure()

ax = fig.add_subplot(131)
hist = cv2.calcHist([chans[2], chans[0]], [0, 1], None, [32, 32], [0, 256, 0, 256])
p  = ax.imshow(hist, interpolation = "nearest")
ax.set_title("2D Color histogram for R and B")
plt.colorbar(p)
plt.show()

cv2.waitKey(0)
