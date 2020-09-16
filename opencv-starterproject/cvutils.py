from matplotlib import pyplot as plt
import numpy as np
import argparse
import cv2

def parseBasicImageArg():
    ap = argparse.ArgumentParser()
    ap.add_argument('-i', '--image', required = True, help = "Path to the image")
    args = vars(ap.parse_args())
    return args

def readImageFromArgs(args):
    image = cv2.imread(args['image'])
    return image

def oneToThreeChannels(channel):
    zeros = np.zeros(channel.shape[:2], dtype = "uint8")
    merged_channels = cv2.merge([zeros, zeros, channel])
    return merged_channels
