#!/bin/python
import numpy
import os
import cPickle
from sklearn.cluster.k_means_ import KMeans
import sys

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print "Usage: {0} vocab_file, file_list".format(sys.argv[0])
        print "vocab_file -- path to the vocabulary file"
        print "file_list -- the list of videos"
        exit(1)

    vocab_file = sys.argv[1]
    file_list = sys.argv[2]

    # load stop words
    stops = {} # dictionary for better hashing
    stops_fd = open("stop-word-list.txt")
    for sto in stops_fd.readlines():
        s = sto.strip().lower()
        stops[s] = 1
    stops_fd.close()

    # load vocab
    vocab = {} # dictionary for better hashing
    vocab_fd = open(vocab_file, "r")
    for voc in vocab_fd.readlines():
        v_list = voc.strip().lower()
        v = v.split(' ')[1]
        if v not in stops:
            vocab[v] = 1
    vocab_fd.close()

    # value is index of word
    i = 0
    for word in vocab:
        vocab[word] = i
        i += 1

    # build bag-of-words representation
    vocab_size = len(vocab)
    file_list_fd = open(file_list, 'r')
    for fil in file_list_fd.readlines():
        file_id = fil.strip()
        path = "asr/" + "11775_asr" + file_id + ".ctm"

        # open output file
        out_file = "asrfeat/" + file_id
        out_file_fd = open(out_file, "w+")

        histogram = numpy.zeros(vocab_size)

        if not os.path.exists(path):
            # out_file_fd.write("-1\n") # write all zeros????
            pass

        else:
            asr_file_fd = open(path, 'r')
            for line in asr_file_fd.readlines():
                li = line.strip()
                li_list = li.split(' ')
                word = li_list[4]
                if word in vocab:
                    histogram[vocab[word]] += 1

            # generate output string
            out_line = str(histogram[0])
            for j in range(1, len(histogram)):
                out_line = out_line + ";" + histogram[j]
            out_file_fd.write(out_line + "\n")

        out_file_fd.close()


    print "ASR features generated successfully!"