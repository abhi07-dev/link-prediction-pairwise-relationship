import csv

from data.parser import get_in_out_dicts
from data.generator import data_path, num_of_pos_samples
from old.local import *


def read_instances():
    instances = list()

    with open('instances.txt', 'r') as ins:
        for i in range(2 * num_of_pos_samples):
            a, b = [int(el) for el in ins.readline().split('\t')]
            instances.append((a, b))
    return instances

def read_test_instances():
    instances = list()

    with open('test-public.txt', 'r') as ins:
        ins.readline()
        for i in range(2000):
            _, a, b = [int(el) for el in ins.readline().split('\t')]
            instances.append((a, b))
    return instances

def read_labels(filepath):
    labels = list()
    with open(filepath, 'r') as lbl:
        for i in range(2 * num_of_pos_samples):
            label = int(lbl.readline())
            labels.append(label)
    return labels

def read_features(filepath):
    features = list()

    with open(filepath, newline='') as f:
        reader = csv.reader(f)
        count = 0
        for row in reader:
            if count > 0:
                features.append([int(i) for i in row])
            count += 1

    return features

# def read_test_features():
#     features = list()
#
#     with open('data/test_features.csv', newline='') as f:
#         reader = csv.reader(f)
#         count = 0
#         for row in reader:
#             if count > 0:
#                 features.append([int(i) for i in row])
#             count += 1
#
#     return features



def calculate_all_features(x, inbound, outbound):
    # get number of edges: a_in, a_out, b_in, b_out.
    features = calculate_simple_features(x, inbound, outbound)
    features = calculate_common_outbound_neighbours(x, inbound, outbound, features)
    features = calculate_common_inbound_neighbours(x, inbound, outbound, features)
    features = calculate_common_a_out_b_in_neighbours(x, inbound, outbound, features)
    features = does_edge_b_to_a_exist(x, inbound, outbound, features)
    features = calculate_mutual_two_way_edges_for_a(x, inbound, outbound, features)

    # TODO Please, call here new metrics you created in metrics/.
    # NOTE: import first and add features as fourth parameter for all next calls

    return features


if __name__ == '__main__':
    x, y = read_instances(), read_labels("labels.txt")
    inbound, outbound, peers = get_in_out_dicts(data_path)

    features = calculate_all_features(x, inbound, outbound)

    with open('features.csv', 'w+', newline='') as csvfile:
        fieldnames = list(features[0].keys())

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel', quotechar='"',
                                quoting=csv.QUOTE_NONNUMERIC)

        writer.writeheader()
        for value in features:
            writer.writerow(value)

    test_features = calculate_all_features(read_test_instances(), inbound, outbound)
    with open('test_features.csv', 'w+', newline='') as csvfile:
        fieldnames = list(test_features[0].keys())

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel', quotechar='"',
                                quoting=csv.QUOTE_NONNUMERIC)

        writer.writeheader()
        for value in test_features:
            writer.writerow(value)
