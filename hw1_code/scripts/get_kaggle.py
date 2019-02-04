import sys

# compare confidence score and get label with highest confidence score


def get_all_confidence_score(file_fd):
    res = []
    for conf in file_fd.readlines():
        confidence = conf.strip()
        res.append(float(confidence))
    return res


if __name__ == '__main__':
    example_list = sys.argv[1]
    p0_file = sys.argv[2]
    p1_file = sys.argv[3]
    p2_file = sys.argv[4]
    out_file = sys.argv[5]

    example_list_fd = open(example_list, "r")
    p0_file_fd = open(p0_file, "r")
    p1_file_fd = open(p1_file, "r")
    p2_file_fd = open(p2_file, "r")
    out_file_fd = open(out_file, "w+")

    # get list of video ids:
    name_list = []
    for line in example_list_fd.readlines():
        lin = line.strip()
        name = lin.split(' ')[0]
        name_list.append(name)

    # get highest confidence scores
    p0_conf = get_all_confidence_score(p0_file_fd)
    p1_conf = get_all_confidence_score(p1_file_fd)
    p2_conf = get_all_confidence_score(p2_file_fd)

    assert(len(p0_conf) == len(p1_conf) and len(p1_conf) == len(p2_conf))

    labels = []
    # get label with highest confidence
    for i in range(len(p0_conf)):
        temp = [p0_conf[i], p1_conf[i], p2_conf[i]]
        labels.append(temp.index(max(temp)) + 1)

    print labels
    print name_list

    # write to output file
    for j in range(len(p0_conf)):
        out_file_fd.write(name_list[j] + "," + str(labels[j]) + "\n")

    example_list_fd.close()
    p0_file_fd.close()
    p1_file_fd.close()
    p2_file_fd.close()
    out_file_fd.close()
