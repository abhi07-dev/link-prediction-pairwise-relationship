import networkx as nx
import matplotlib.pyplot as plt

digraph = nx.DiGraph()
digraph.add_edges_from([(1, 2), (1, 8), (2, 8), (8, 1), (8, 4), (4, 2)])
ugraph = digraph.to_undirected()

nx.draw_networkx(digraph, node_color='w')
nx.draw_networkx_labels(digraph, pos=nx.circular_layout(digraph))
# plt.show()

print(nx.to_numpy_matrix(digraph))
print(nx.nodes(digraph))
print(nx.edges(digraph))

# print(nx.to_numpy_matrix(nx.subgraph(digraph, nx.neighbors(ugraph, 1))))
# print(nx.hits_numpy(ugraph))

nx.write_gpickle(digraph, 'test.gpickle')
digraph = nx.read_gpickle("test.gpickle")
print(nx.to_numpy_matrix(digraph))
print(nx.nodes(digraph))
print(nx.edges(digraph))