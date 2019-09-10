from sklearn.utils import shuffle
from data.parser import get_in_out_dicts

data_path = "../../data_smile/"
num_of_pos_samples = 20000

def generate_data():
    inbound, outbound, _ = get_in_out_dicts(data_path)
    # pos_peers = list()
    one_inb=list()
    more_inbound = list()
    outbound_items = list(outbound.items())
    inbound_items = list(inbound.items())
    for a, b_list in outbound_items:
        if len(b_list) > 0:
            if len(b_list) >= 100:
                b_samples = shuffle(b_list, n_samples=100)
            else:
                b_samples = b_list

            for b in b_samples:
                if len(inbound[b]) == 1:
                    one_inb.append(b)
                else:
                    more_inbound.append(b)

    pos_samples = shuffle(one_inb, n_samples=num_of_pos_samples * 0.083)
    pos_samples += shuffle(more_inbound, n_samples=num_of_pos_samples * (1-0.083))

    # # Adding crawled nodes as A in negative samples
    # negative_peers = list()
    # for a, b_list in outbound_items:
    #     for i in range(5):
    #         node, _ = random.choice(inbound_items)
    #         if node not in b_list:
    #             negative_peers.append((a, node))
    # neg_samples1 = shuffle(negative_peers, n_samples=num_of_pos_samples)
    #
    # negative_peers = list()
    # # Adding non-crawled nodes as A assuming there is
    # for b, a_list in inbound.items():
    #     for i in range(5):
    #         a, _ = random.choice(inbound_items)
    #         if a not in a_list:
    #             negative_peers.append((a, b))
    # neg_samples2 = shuffle(negative_peers, n_samples=num_of_pos_samples)
    #
    # neg_samples = shuffle(neg_samples1 + neg_samples2, n_samples=num_of_pos_samples)

    xs = pos_samples # + neg_samples
    # ys = [1 for _ in range(num_of_pos_samples)] + [0 for _ in range(num_of_pos_samples)]
    # xs, ys = shuffle(xs, ys)

    with open('instances.txt', 'w+') as ins:
        for x in xs:
            ins.writelines(str(x[0]) + '\t' + str(x[1]) + '\n')

    # with open('labels.txt', 'w+') as lbl:
    #     for y in ys:
    #         lbl.write(str(y) + '\n')


if __name__ == '__main__':
    generate_data()

    # I am keeping this chunk if I need it in future
    # # Write all positive cases
    # with open(data_path + 'positive.csv', 'w', newline='') as csvfile:
    #     fieldnames = [
    #         'A',
    #         'B',
    #         'label'
    #     ]
    #     writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel', quotechar='"',
    #                             quoting=csv.QUOTE_NONNUMERIC)
    #     writer.writeheader()
    #     for a, b_list in outbound.items():
    #         for b in b_list:
    #             writer.writerow({
    #                 'A': a,
    #                 'B': b,
    #                 'label': 1
    #             })
    #
    # # Write all negative cases
    # with open(data_path + 'negative.csv', 'w', newline='') as csvfile:
    #     fieldnames = [
    #         'A',
    #         'B',
    #         'label'
    #     ]
    #     inbound_items = list(inbound.items())
    #     writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel', quotechar='"',
    #                             quoting=csv.QUOTE_NONNUMERIC)
    #     writer.writeheader()
    #     for b, a_list in inbound.items():
    #         if len(a_list) <= 1:
    #             for i in range(5):
    #                 a, _ = random.choice(inbound_items)
    #                 if a not in a_list:
    #                     writer.writerow({
    #                         'A': a,
    #                         'B': b,
    #                         'label': 0
    #                     })