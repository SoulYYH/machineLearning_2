import argparse
import csv
import math
import sys
from collections import Counter

def entropy(data, target_classes):
    attribute_value = {}

    for c in data:
        if c not in attribute_value.keys():
            attribute_value[c] = 1
        else:
            attribute_value[c] += 1

    entropy_data = 0
    samples = float(len(data))

    if len(attribute_value.keys()) == 1:
        return 0

    for keys in attribute_value.keys():
        entropy_data += -(attribute_value[keys] * math.log(attribute_value[keys]/samples, target_classes) / samples)

    return entropy_data


def average_weighted_entropy(attribute_entropy):
    # given a dictionary of {attr1 : [entropy, #of samples]}
    # print(attribute_entropy)

    numberSamples = 0

    for key in attribute_entropy.keys():
        numberSamples += attribute_entropy[key][1]

    weightedEntropy = {}

    weightedEntropy['weighted_entropy'] = 0

    for key in attribute_entropy.keys():
        # print("for key: ", key)
        if key not in weightedEntropy.keys():
            weightedEntropy[key] = attribute_entropy[key]

        weightedEntropy['weighted_entropy'] += (attribute_entropy[key][1] * attribute_entropy[key][0]/numberSamples)

    # ("weighted entropy", weightedEntropy)
    return weightedEntropy


def decision_node_infromation_gain(data, att_processed, att_given, entropy_decision_node, target_class):

    # keeps the count of the attributes which are already been processed.
    attributes_left = list(set(att_given) - set(att_processed))

    # print("here")

    information_gain = {}
    # print(attributes_left)
    for i in attributes_left:
        # print("attribute: ", i)
        entropy = average_weighted_entropy(attribute_entropy(data, i, target_class))
        # print("here")
        information_gain[i] = [entropy_decision_node - entropy['weighted_entropy'], entropy]

    return information_gain

def attribute_entropy(data, attribute, target_class):

    attribute_split_values = {}
    target_class_set = set()

    for num, c in enumerate(data):
        target_class_set.add(c[-1])
        if c[attribute] not in attribute_split_values.keys():
            attribute_split_values[c[attribute]] = [c[-1]]
        else:
            attribute_split_values[c[attribute]].append(c[-1])

    for keys in attribute_split_values.keys():
        # ("attribute", target_class_set)
        attribute_split_values[keys] = [entropy(attribute_split_values[keys], target_class), len(attribute_split_values[keys])]

    return attribute_split_values

def data_split(data, attribute):

    dataset_split = {}

    for k in data:
        if k[attribute] not in dataset_split.keys():
            dataset_split[k[attribute]] = [k]
        else:
            dataset_split[k[attribute]].append(k)

    return dataset_split


global global_attribute
global_attribute = []

def recursion_tree(data, decision_node, list_attributes, attributes_processed, target_class, attribute_given = 0, key_given = 0):

    level = decision_node[0]
    entropy_decision_node = decision_node[2]

    if entropy_decision_node == 0 or len(global_attribute) - len(list_attributes) == 0:
        # ("Entropy 0 and level: ", level + 1, data[0][-1])
        # return [level+1, "att{}={}".format(max_infoGainAttr, key), e[key][0], 'no_leaf']
        # ("_________________>", [level, "att{}={}".format(attribute_given, key_given), entropy_decision_node, data[0][-1]])
        return [[level, "att{}={}".format(attribute_given, key_given), entropy_decision_node, data[0][-1]]]

    # for attribute in list_attributes:

    information_gain = decision_node_infromation_gain(data, attributes_processed, list_attributes, entropy_decision_node, target_class)


    # (information_gain)

    # ("--->")
    # print(attributes_processed, global_attribute)
    # print(information_gain)
    temp = list(information_gain.keys())[0]

    # print(global_attribute)
    # print(information_gain.keys())
    # (decision_node)
    # for i in decision_node:
    #     (i)


    for k in information_gain.keys():
        if information_gain[k][0] > information_gain[temp][0]:
            temp = k

    max_infoGainAttr, max_infoGain, e = temp, information_gain[temp][0], information_gain[temp][1]

    # ("max_inforgain_attribute: {} and max_infogain: {}".format(max_infoGainAttr, max_infoGain))
    # ("max_inforgain_attribute: {} ".format(max_infoGainAttr))
    # ("entropy-->", e)


    data_split_att = data_split(data, max_infoGainAttr)

    # (data_split_att.keys())
    #
    # ('-------')

    # attributes_processed = [max_infoGainAttr]

    # global global_attribute
    global_attribute.append(max_infoGainAttr)

    return_nodes = [decision_node]

    # ("return nodes")
    # (return_nodes)
    level_node = level+1
    # attributes_processed = [max_infoGainAttr]
    for key in list(data_split_att.keys())[::-1]:
        # ("for the key:", key, e[key], "attribute: ", max_infoGainAttr)
        # ("***for the attribute{}={}***".format(max_infoGainAttr, key), e[key][0])

        # decision_node.append([level+1, "att{}={}".format(max_infoGainAttr, key), e[key][0], 'no_leaf'])
        # (decision_node)
        # attributes_processed
        # attributes_processed.pop
        # ("Attributes: {} processed {} ".format(list_attributes, global_attribute))
        start_node = []
        # level += 1
        if e[key][0] == 0:

            # ("returning")
            # ("Keys left", data_split_att.keys())
            t = recursion_tree(data_split_att[key], [level_node, 0, e[key][0]], list_attributes, global_attribute, target_class, max_infoGainAttr, key)


            # attributes = t['attributes']
            start_node += t
            # ("start_node:" , start_node)
            # attributes_processed.pop(-1)
            # (";sladjflsadjk")

        else:
            # (level_node)
            # attributes_processed.pop(-1)
            _temp = [level_node, "att{}={}".format(max_infoGainAttr, key), e[key][0], 'no_leaf']
            t = recursion_tree(data_split_att[key], _temp, list_attributes, global_attribute, target_class, max_infoGainAttr, key)

            # []
            # [[], [], []]
            start_node = [[level_node, "att{}={}".format(max_infoGainAttr, key), e[key][0], 'no_leaf']]
            #
            start_node += t
            # attributes_processed.pop(-1)


        # (start_node)


        # if e[key][0] == 0:
        #     leaf_nodes.append([level+1, "att{}={}".format(max_infoGainAttr, key), e[key][0], data[0][-1]])
        # else:

        # leaf_nodes = [level+1, "att{}={}".format(max_infoGainAttr, key), e[key][0], 'no_leaf']
        # leaf_nodes.append(recursion_tree(data_split_att[key], leaf_nodes, list_attributes, attributes_processed, target_class, max_infoGainAttr, key))
        #

        return_nodes += start_node
        # attributes_processed.pop(-1)
        # ("$$$$$$$$")
        # (leaf_node)
        # decision_node.append(leaf_nodes)

        # (decision_node)
        # ("******")

    # ("^^^^^^^^^^^returning nodes^^^^^^^^^^^^^^")
    global_attribute.pop(-1)
    # (return_nodes[1:])
    return return_nodes[1:]



    # (data_split_att['low'])
    # try:
    #     recursion_tree(data_split_att['high'], [0, 0, 0.807755925], [0, 1, 2, 3, 4], [])
    # except:
    #     recursion_tree(data_split_att['more'], [0, 0, 0.807755925], [0], [])
    # (k, information_gain[k])
    # (temp, information_gain[temp])

    # a dict. which has the attribute w max. information gain and the data for the attribute.
    # max_information_gain = {}
    pass


import numpy as np

if __name__ == '__main__':
    # sys.stdout = open("C:/Users/Krishna/PycharmProjects/machineLearning_2/test.txt", "wt")

    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type = str)

    args = parser.parse_args()

    path = args.data

    training_data = []
    target_class = set()
    temp_data = []
    with open(path) as f:
        cf = csv.reader(f)
        for row in cf:
            try:
                if len(row) != 0:
                    training_data.append(row)
                    target_class.add(row[-1])
                    temp_data.append(row[-1])
            except:
                pass

    decision_tree = []
    decision_tree.append([0, 'root', entropy(temp_data, len(target_class)), 'no_leaf'])

    # print(decision_tree)
    list_attributes = [i for i in range(len(training_data[:][0]) - 1)]

    # print(list_attributes)
    # (decision_tree)
    # (decision_node(training_data, [], list_attributes, 0.602870485))
    # print(training_data[-1])
    # print(decision_tree[0])
    t = recursion_tree(training_data, decision_tree[0], list_attributes, [], len(target_class))

    # for i in t:
    #     (i)

    decision_tree += t

    for i in decision_tree:
        print(str(i[0])+ "," + str(i[1]) +","+ str(i[2]) + "," + str(i[3]))

    # save = np.array(decision_tree, dtype=object)
    #
    # np.savetxt("C:/Users/Krishna/PycharmProjects/machineLearning_2/output.csv", save, delimiter=',', encoding='utf-8', fmt='%s')
    # (len(t))

    # (t[0])
    # (t[1][5])
    # (len(t[0]))
    # (len(t[0]))

    # datasplit = data_split(training_data, 5)
    #
    # datasplit2 = data_split(datasplit['high'], 0)
    #
    # datasplit3 = data_split(datasplit2['high'], 2)
    #
    # for k in datasplit3.keys():
    #     (k, datasplit3[k][:5], len(datasplit3[k]))


    # ("Hello World")

    # sys.stdout.close()






