import pandas as pd

from data.generator import data_path
from data.parser import get_in_out_dicts

inbound, outbound, undirected = get_in_out_dicts(data_path)
instances = list()

with open('new_instances.txt', 'r') as ins:
    ins.readline()
    for i in range(20000):
        instances.append([el for el in ins.readline().split('\t')])


res = list()
ids = 1
for a, b in instances:

    common_neighbours = len(undirected[a] & undirected[b])
    union = len(undirected[a] | undirected[b])
    res.append((ids, float(common_neighbours) / union))
    ids = ids + 1

_, max_common_neghbours = max(res, key=lambda x: x[1])
res = [(id, common_neghbours/max_common_neghbours) for id, common_neghbours in res]

with open('predict_jaccard111.csv', 'w+') as pred_file:
    pred_file.write('Id,Prediction\n')
    for id, res in res:
        pred_file.write(str(id) + ',' + str(res) + '\n')
