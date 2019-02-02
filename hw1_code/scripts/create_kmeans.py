#!/bin/python
import numpy
import os
import cPickle
from sklearn.cluster.k_means_ import KMeans
import sys
# Generate k-means features for videos; each video is represented by a single vector

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print "Usage: {0} kmeans_model, cluster_num, file_list".format(sys.argv[0])
        print "kmeans_model -- path to the kmeans model"
        print "cluster_num -- number of cluster"
        print "file_list -- the list of videos"
        exit(1)

    kmeans_model = sys.argv[1]
    cluster_num = int(sys.argv[2])
    file_list = sys.argv[3]

    # load the kmeans model
    kmeans = cPickle.load(open(kmeans_model,"rb"))
    print("Successfully loaded K-means model.")

    # process each audio file
    file_list_fd = open(file_list, "r")
    for name in file_list_fd.readlines():
        name_strip = name.strip()
        mfcc_file = "mfcc/" + name_strip + ".mfcc.csv"

        # open output file
        out_file = "kmeans-features/" + name_strip
        out_file_fd = open(out_file, "w+")

        # if no mfcc file (no audio)
        if not os.path.exists(mfcc_file):
            # write -1 to the file?
            out_file_fd.write("-1\n")
            continue

        # mfcc file exists
        else:
            # create histogram, each represent one k-means feature
            histogram = numpy.zeros(cluster_num)

            # read in mfcc and predict k-means, then create histograms
            mfcc_features = numpy.genfromtxt(mfcc_file, dtype=numpy.float64, delimiter=";")
            kmeans_features = kmeans.predict(mfcc_features)

            for f in kmeans_features:
                histogram[f] += 1

            # TO DO: normalize features?????

            # write histogram to output file
            histogram_str = ';'.join([str(t) for t in v])
            histogram_str = histogram_str + "\n"
            out_file_fd.write(histogram_str)

        out_file_fd.close()

    file_list_fd.close()

    print "K-means features generated successfully!"
