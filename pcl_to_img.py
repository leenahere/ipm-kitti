from __future__ import print_function
import os
import sys
import argparse
import cv2
import numpy as np


def inverse_perspective_mapping(prefix, iterator):
    label_image = cv2.imread('/home/mechlab/kitti/data_road/training/gt_image_2/' + prefix + '_road_' + iterator + '.png')
    src = np.array([[152, 374], [807, 374], [557, 206], [656, 206]], np.float32)
    dst = np.array([[61, 399], [117, 399], [61, 74], [117, 74]], np.float32)

    M = cv2.getPerspectiveTransform(src, dst)
    warp = cv2.warpPerspective(label_image.copy(), M, (200, 400))
    cv2.imwrite('../../label_data_transformed/labels/ground_truth_transformed_' + prefix + '_' + iterator + '.png', warp)


def main():
    prefix_list = ['um', 'umm', 'uu']
    for prefix in prefix_list:
        for i in range(0, 98):
            iterator = "%06d" % (i)
            blank_image = np.zeros((400, 200), np.uint8)
            try:
                filepath = '../../data_velodyne/testing_converted_pcl/' + prefix + '_' + iterator + '.bag'
                with open(filepath) as fp:
                    line = fp.readline()
                    cnt = 1
                    while line:
                        if not line.strip()[0].isdigit():
                            line = fp.readline()
                            cnt += 1
                            continue

                        x, y, z, i = map(float, line.strip().split(" "))

                        if 6 <= x < 46 and -10 <= y < 10:
                            blank_image[399 - int((x - 6) * 10), 199 - int((y + 10) * 10)] = i * (2 ** 8 - 1)
                        line = fp.readline()
                        cnt += 1

                cv2.imwrite('../../label_data_transformed/testing/' + prefix + '_' + iterator + '.png', blank_image)
                #inverse_perspective_mapping(prefix, iterator)
            except:
                pass


if __name__ == '__main__':
    main()
