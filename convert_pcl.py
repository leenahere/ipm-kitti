from __future__ import print_function
import os
import sys
import argparse


def main():
    prefix_list = ['um', 'umm', 'uu']
    for prefix in prefix_list:
        for i in range(0, 98):
            iterator = "%06d" % (i)
            try:
                cmd = '../cmake-build-debug/bin/kitti2pcd --infile ../../data_velodyne/testing/velodyne/' + prefix + '_' + iterator + '.bin --outfile ../../data_velodyne/testing_converted_pcl/' + prefix + '_' + iterator + '.bag'
                os.system(cmd)
            except:
                pass


if __name__ == '__main__':
    main()
