from __future__ import print_function
import os
import sys
import argparse
import cv2
import numpy as np


def inverse_perspective_mapping():
    label_image = cv2.imread('/home/mechlab/kitti/data_road/training/gt_image_2/umm_road_000017.png')
    feature_image = cv2.imread('/home/mechlab/kitti/kitti-pcl/scripts/laser_image.png')
    #src = np.array([[440, 372], [800, 372], [592, 182], [578, 182]], np.float32)
    #dst = np.array([[71, 399], [125, 399], [107, 60], [43, 60]], np.float32)
    #src = np.array([[372, 440], [372, 800], [182, 592], [182, 578]], np.float32)
    #dst = np.array([[399, 71], [399, 125], [60, 107], [60, 43]], np.float32)
    #src = np.array([[440, 372], [800, 372], [440, 182], [800, 182]], np.float32)
    #dst = np.array([[71, 399], [125, 399], [71, 60], [125, 60]], np.float32)
    src = np.array([[152, 374], [807, 374], [557, 206], [656, 206]], np.float32)
    dst = np.array([[61, 399], [117, 399], [61, 74], [117, 74]], np.float32)

    M = cv2.getPerspectiveTransform(src, dst)
    warp = cv2.warpPerspective(label_image.copy(), M, (200, 400))
    print(feature_image.shape)
    print(warp.shape)
    added_image = cv2.addWeighted(feature_image,0.6,warp,0.4,0)
    cv2.imshow('img', added_image)
    cv2.waitKey(0)
    cv2.destoryAllWindows()


def main():
    max = 0
    blank_image = np.zeros((400, 200), np.uint8)
    filepath = '../../data_velodyne/converted_pointclouds/umm_000017.bag'
    with open(filepath) as fp:
        line = fp.readline()
        cnt = 1
        while line:
            if not line.strip()[0].isdigit():
                line = fp.readline()
                cnt += 1
                continue

            x, y, z, i = map(float, line.strip().split(" "))
            max = max if max > i else i

            if 6 <= x < 46 and -10 <= y < 10:
                blank_image[399 - int((x - 6) * 10), 199- int((y + 10) * 10)] = i*(2 ** 8 - 1)
            line = fp.readline()
            cnt += 1


    cv2.imwrite('laser_image.png', blank_image)
    # cv2.imshow("img.png", blank_image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    print(max)


if __name__ == '__main__':
    main()
    inverse_perspective_mapping()
