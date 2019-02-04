#!/bin/python 

import numpy
import os
from sklearn.svm.classes import SVC
import cPickle
import sys

# Apply the SVM model to the testing videos; Output the score for each video

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print "Usage: {0} model_file feat_dir feat_dim output_file".format(sys.argv[0])
        print "model_file -- path of the trained svm file"
        print "feat_dir -- dir of feature files"
        print "feat_dim -- dim of features; provided just for debugging"
        print "output_file -- path to save the prediction score"
        exit(1)

    model_file = sys.argv[1]
    feat_dir = sys.argv[2]
    feat_dim = int(sys.argv[3])
    output_file = sys.argv[4]

    # get test list
    test_list = '/home/ubuntu/11775-hw1/all_test_fake.lst'
    # test_list = '/home/ubuntu/11775-hw1/all_val.lst'
    test_list_file_fd = open(test_list, "r")
    tests = []
    for tes in test_list_file_fd.readlines():
        test = tes.strip()
        line = test.split(' ')
        tests.append(line[0])
    test_list_file_fd.close()

    # load svm model and write prediction to output
    model_file_fd = open(model_file, "rb")
    svm_model = cPickle.load(model_file_fd)
    output_file_fd = open(output_file, "w")

    for v in tests:
        if os.path.exists(feat_dir + v):
            if os.stat(feat_dir + v).st_size == 0:
                feat_vector = numpy.zeros([1, feat_dim], dtype=numpy.float32).reshape(1, -1)
            else:
                feat_vector = numpy.genfromtxt(feat_dir + v, dtype=numpy.float32, delimiter=";").reshape(1, -1)
        else:
            # if no feature available, simply feed in zeros
            feat_vector = numpy.zeros([1, feat_dim], dtype=numpy.float32).reshape(1, -1)
            # feat_vector = numpy.zeros(feat_dim, dtype=numpy.float32)

        result = svm_model.decision_function(feat_vector)
        output_file_fd.write(str(result[0]) + '\n')

    model_file_fd = open(model_file, "rb").close()
    output_file_fd.close()

    print 'SVM prediction done successfully for event %s!'

