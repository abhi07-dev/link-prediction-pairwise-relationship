import numpy as np

INPUT_FILE = "adamic.csv"
OUTPUT_FILE = "adamic_norm.csv"

if __name__ == '__main__':
    instances = list()

    with open(INPUT_FILE, 'r') as ins:
        ins.readline()
        for i in range(2000):
            tmp = ins.readline().split(',')
            value = float(tmp[1])
            instances.append(value)
        instances = np.array(instances)
    instances = instances / np.max(instances)



    # max_sim = max(instances, key=lambda x: x[1])
    # res = [(id, sim/max) for id, sim in instances]

    with open(OUTPUT_FILE, 'w+') as pred_file:
        pred_file.write('Id,Prediction\n')
        id = 1
        for proba in instances:
            pred_file.write(str(id) + ',' + str(proba) + '\n')
            id += 1