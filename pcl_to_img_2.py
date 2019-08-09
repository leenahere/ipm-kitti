from __future__ import print_function
import os
import sys
import argparse
import cv2
import numpy as np


def main():
    blank_image = np.zeros((400, 200), np.uint8)
    for i in range(1, 26):
        try:
            with open('pcl_clouds_5/cloud_' + str(i)) as fp:
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

            cv2.imwrite('images/pcl_' + str(i) + '.png', blank_image)
        except:
            pass

# def main():
#     blank_image = np.zeros((400, 200), np.uint8)
#     for i in range(0,7):
#         try:
#             with open('pcl_clouds_4/' + str(i)) as fp:
#                 line = fp.readline()
#                 cnt = 1
#                 while line:
#                     if not line.strip()[0].isdigit():
#                         line = fp.readline()
#                         cnt += 1
#                         continue
#
#                     x, y, z, i = map(float, line.strip().split(" "))
#
#                     if 6 <= x < 46 and -10 <= y < 10:
#                         blank_image[399 - int((x - 6) * 10), 199 - int((y + 10) * 10)] = i * (2 ** 8 - 1)
#                     line = fp.readline()
#                     cnt += 1
#
#             cv2.imwrite('images/pcl_' + str(i) + '.png', blank_image)
#         except:
#             pass

# def main():
#     blank_image = np.zeros((400, 200), np.uint8)
#     for i in range(1,2):
#         try:
#             with open('test_cloud') as fp:
#                 line = fp.readline()
#                 cnt = 1
#                 while line:
#                     if not line.strip()[0].isdigit():
#                         line = fp.readline()
#                         cnt += 1
#                         continue
#
#                     x, y, z, i = map(float, line.strip().split(" "))
#
#                     if 6 <= x < 46 and -10 <= y < 10:
#                         blank_image[399 - int((x - 6) * 10), 199 - int((y + 10) * 10)] = i * (2 ** 8 - 1)
#                     line = fp.readline()
#                     cnt += 1
#
#             cv2.imwrite('test_cloud.png', blank_image)
#         except:
#             pass


if __name__ == '__main__':
    main()