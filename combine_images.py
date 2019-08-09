import cv2
import numpy as np

prefix_list = ['um', 'umm', 'uu']
for theta in range(-30, 30, 5):
    for prefix in prefix_list:
        for i in range(0, 2):
            iterator = "%06d" % i
            label = cv2.imread('../../label_data_transformed_rot/labels/ground_truth_transformed_' + prefix + '_' + iterator + '_' + str(theta) + '.png')
            feature = cv2.imread('/home/mechlab/kitti/label_data_transformed_rot/features/' + prefix + '_' + iterator + '_' + str(theta) + '.png')

            result = cv2.addWeighted(feature, 0.6, label, 0.4, 0)
            cv2.imwrite('../../label_data_transformed_rot/combined/' + prefix + '_' + iterator + '.png', result)
