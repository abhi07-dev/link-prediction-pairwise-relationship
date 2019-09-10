- Create m-fold data to cross-validate
- Build evaluator AUC + ROC
- Generalizing technique: random forest, logistic regression, SVM, ANN, etc.
- Find interesting patterns in data
- Create features as much as possible

### Hypothesis:
- "Rich get richer". If node B's inbound degree is high and A's outbound degree is also high, A->B is more probable.

### Stats:
- Number of edges 24004361
- Number of nodes with inner edges 4867136
- Number of nodes with outer edges 20000 (only 19570 has at least 1 outerEdge)
- Nodes with at least 1 inner and 1 outer edges: 19570
- So 430 nodes are crawled but don't have outer edges but only inner edges. Among them, 30 nodes have more than 100 followers
- 2858090 nodes don't have outeredge and only 1 inner edge / 4867136=58.7%
- Those 430 users might be dead links
- 1631 B nodes don't have outbound neighbours => they are not crawled.

### About test input:
- All A nodes have at least both inbound and outbound edges
- 1631 of Bs have no outbound, 356 have more than 10 outbounds so only 13 have less than 10 outbounds
- So all A nodes are crawled ones, most of B nodes are not crawled nodes.
- We should keep clustering them and if group's elements close to 1000, I assume it highly correlates with edges.
- In 156 test cases, there is an edge from B to A
- 166 B nodes has only 1 inbound and no outbound
- 584 N nodes has less than 10 inbound and no outbound
- If B node follows A (156) and A has many following back behaviour (149), then probably there is an edge.

### About training
- We should learn nature of network here as well

### Other
- We should keep writing about our trials and results to write more informative & interesting report

### Lab results
- When taking only common_a_in_b_out similarity measure to predict, AUC=0.77832
- When tried with common_in_neighbours, AUC=0.78619
- When tried with undirected graph, common neighbours' AUC=0.79770
- Jaccard similarity of A and B with undirected graph gave AUC=0.82329
- Jaccard (3) with all avg is giving AUC=0.88667; with avg when value is nonzero gave little  
  bit better result 0.88817 which I believe it is noise

