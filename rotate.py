from __future__ import print_function
import os
import sys
import argparse
import cv2
import numpy as np
from math import sin, cos, radians
import imutils

offset = np.array([25, 0, 0])


def h_stretch_image(image, stretch_value):
    n0, n1, channel = image.shape
    stretch_value = int(stretch_value)

    left_side = image[0:n0, 0, :]
    right_side = image[0:n0, n1 - 1, :]

    left_stretch = np.zeros((n0, stretch_value, channel))
    right_stretch = np.zeros((n0, stretch_value, channel))

    for i in range(stretch_value):
        left_stretch[:, i, :] = left_side
        right_stretch[:, i, :] = right_side

    end_image = np.hstack((left_stretch, image))
    end_image = np.hstack((end_image, right_stretch))

    return end_image


def v_stretch_image(image, stretch_value):
    n0, n1, channel = image.shape
    stretch_value = int(stretch_value)

    left_side = image[0:n0, 0, :]
    right_side = image[0:n0, n1 - 1, :]

    left_stretch = np.zeros((n0, stretch_value, channel))
    right_stretch = np.zeros((n0, stretch_value, channel))

    for i in range(stretch_value):
        left_stretch[:, i, :] = left_side
        right_stretch[:, i, :] = right_side

    end_image = np.vstack((left_stretch, image))
    end_image = np.vstack((end_image, right_stretch))

    return end_image


def rot(theta):
    return np.array([[cos(theta), sin(theta), 0], [-sin(theta), cos(theta), 0], [0, 0, 1]])


def transform(x, y, z, theta):
    vec = np.array([x, y, z])
    vec -= offset
    vec = vec.dot(rot(theta))
    vec += offset

    return vec[0], vec[1], vec[2]


def inverse_perspective_mapping(prefix, iterator, theta):
    label_image = cv2.imread(
        '/home/mechlab/kitti/data_road/training/gt_image_2/' + prefix + '_road_' + iterator + '.png')

    src = np.array([[152, 374], [807, 374], [557, 206], [656, 206]], np.float32)
    dst = np.array([[61, 399], [117, 399], [61, 74], [117, 74]], np.float32)

    M = cv2.getPerspectiveTransform(src, dst)
    warp = cv2.warpPerspective(label_image.copy(), M, (200, 400))
    rotated = imutils.rotate(warp, theta)
    cv2.imwrite(
        '../../label_data_transformed_rot/labels/ground_truth_transformed_' + prefix + '_' + iterator + '_' + str(
            theta) + '.png', rotated)


def main():
    prefix_list = ['um', 'umm', 'uu']
    j = 0
    for theta in range(-30, 30, 5):
        for prefix in prefix_list:
            for i in range(0, 98):
                j = j + 1
                print(j)

                iterator = "%06d" % (i)
                blank_image = np.zeros((400, 200), np.uint8)
                try:
                    filepath = '/home/mechlab/kitti/data_velodyne/converted_pointclouds/' + prefix + '_' + iterator + '.bag'
                    with open(filepath) as fp:
                        line = fp.readline()
                        cnt = 1
                        while line:
                            if not line.strip()[0].isdigit():
                                line = fp.readline()
                                cnt += 1
                                continue

                            x, y, z, i = map(float, line.strip().split(" "))
                            x, y, z = transform(x, y, z, radians(theta))

                            if 6 <= x < 46 and -10 <= y < 10:
                                blank_image[399 - int((x - 6) * 10), 199 - int((y + 10) * 10)] = i * (2 ** 8 - 1)
                            line = fp.readline()
                            cnt += 1

                    cv2.imwrite(
                        '/home/mechlab/kitti/label_data_transformed_rot/features/' + prefix + '_' + iterator + '_' + str(
                            theta) + '.png', blank_image)
                    inverse_perspective_mapping(prefix, iterator, theta)
                except:
                    pass


if __name__ == '__main__':
    main()

    prefix_list = ['um', 'umm', 'uu']
    for theta in range(-30, 30, 5):
        for prefix in prefix_list:
            for i in range(0, 98):
                iterator = "%06d" % i
                label = cv2.imread('../../label_data_transformed_rot/labels/ground_truth_transformed_' + prefix + '_' + iterator + '_' + str(theta) + '.png')
                feature = cv2.imread('/home/mechlab/kitti/label_data_transformed_rot/features/' + prefix + '_' + iterator + '_' + str(theta) + '.png')

                result = cv2.addWeighted(feature, 0.6, label, 0.4, 0)
                cv2.imwrite('../../label_data_transformed_rot/combined/' + prefix + '_' + iterator + '_' + str(theta) + '.png', result)
