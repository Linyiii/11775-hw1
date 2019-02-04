#!/bin/python 

import numpy
import os
from sklearn.svm.classes import SVC
import cPickle
import sys

# Performs K-means clustering and save the model to a local file

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print "Usage: {0} event_name feat_dir feat_dim output_file".format(sys.argv[0])
        print "event_name -- name of the event (P001, P002 or P003 in Homework 1)"
        print "feat_dir -- dir of feature files"
        print "feat_dim -- dim of features"
        print "output_file -- path to save the svm model"
        exit(1)

    event_name = sys.argv[1]
    feat_dir = sys.argv[2]
    feat_dim = int(sys.argv[3])
    output_file = sys.argv[4]

    # training_label_file = "/home/ubuntu/11775-hw1/all_trn.lst"
    training_label_file = "/home/ubuntu/11775-hw1/combined_train.lst"
    training_label_file_fd = open(training_label_file, 'r')
    training_labels_ori = {}
    for lin in training_label_file_fd.readlines():
        line = lin.strip()
        line_lst = line.split(" ")
        file_id = line_lst[0]
        file_label = line_lst[1]

        # if no label
        if file_label == "NULL":
            continue

        else:
            if file_label == event_name:
                training_labels_ori[file_id] = 1
            else:
                training_labels_ori[file_id] = 0
    training_label_file_fd.close()

    # exclude examples that does not have training features
    training_examples = []
    training_labels = []
    for fi in training_labels_ori:
        if os.path.exists(feat_dir + fi):
            training_examples.append(fi)
            training_labels.append(training_labels_ori[fi])


    # get feature matrix
    training_size_final = len(training_examples)
    feat_matrix = numpy.zeros([training_size_final, feat_dim])
    label_vector = numpy.fromiter(training_labels, dtype=int)
    for i in range(training_size_final):
        if os.stat(feat_dir + training_examples[i]).st_size == 0:
            feat_vector = numpy.zeros(feat_dim, dtype=numpy.float32)
        else:
            feat_vector = numpy.genfromtxt(feat_dir + training_examples[i], dtype=numpy.float32, delimiter=";")
        feat_matrix[i, :] = feat_vector

    # train an svm model and save to output file
    output_file_fd = open(output_file, "w+")
    svm_model = SVC(kernel='linear', class_weight='balanced', cache_size=1000,
                    C=10)  # tune this!!!!!!!!!!!!!!!!!!!!!!

    svm_model.fit(feat_matrix, label_vector)
    cPickle.dump(svm_model, output_file_fd)
    # cPickle.HIGHEST_PROTOCOL needed?
    output_file_fd.close()




    print 'SVM trained successfully for event %s!' % (event_name)