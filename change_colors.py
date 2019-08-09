from __future__ import print_function
import os
import sys
import argparse
import cv2
import numpy as np


def main():
    prefix_list = ['um', 'umm', 'uu']
    for theta in range(-30, 30, 5):
        for prefix in prefix_list:
            for i in range(0, 98):
                iterator = "%06d" % i
                try:
                    label_image = cv2.imread(
                        '../../label_data_transformed_rot/labels/ground_truth_transformed_' + prefix + '_' + iterator + '_' + str(theta) + '.png')
                    filtered_img = label_image[:, :, 0]
                    cv2.imwrite(
                        '../../label_data_transformed_rot/labels_gray/ground_truth_transformed_' + prefix + '_' + iterator + '_' + str(theta) + '.png',
                        filtered_img)
                except:
                    pass


if __name__ == '__main__':
    main()
