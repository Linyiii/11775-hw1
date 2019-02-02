#!/bin/python 

import numpy
import os
from sklearn.cluster.k_means_ import KMeans
import cPickle
import sys

# Performs K-means clustering and save the model to a local file

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: {0} mfcc_csv_file cluster_num output_file".format(sys.argv[0]))
        print("mfcc_csv_file -- path to the mfcc csv file")
        print("cluster_num -- number of cluster")
        print("output_file -- path to save the k-means model")
        exit(1)

    # read cmd lime args
    mfcc_csv_file = sys.argv[1]
    cluster_num = int(sys.argv[2])
    output_file = sys.argv[3]

    # load mfcc features
    mfcc_features = numpy.genfromtxt(mfcc_csv_file, dtype=numpy.float64, delimiter=";")

    # create and execute k-means clustering
    km_model = KMeans(n_clusters=cluster_num)
    km_model.fit(mfcc_features)
    print("K-means trained successfully!")

    # save model
    out_fd = open(output_file, "wb")
    cPickle.dump(km_model, out_fd) #cPickle.HIGHEST_PROTOCOL needed?
    out_fd.close()
    print("K-means saved successfully!")
