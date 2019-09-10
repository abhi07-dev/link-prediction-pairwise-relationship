# Introduction
**This is the implementation for the first project of Statistical Machine Learning Course COMP90051, 2018.**  
Link prediction is one of the fundamental problems in social network analysis. The social network can be visualized as a graph, where nodes correspond to the entities and the edges (or links) represents relationships/interactions between entities. Since these networks are highly sparse in nature and the data completeness can’t be ensured, forecasting a new connection based on the existing information is a task of great importance. In this project, the student groups are provided with social network data from Twitter, which consists of 20,000 crawled nodes (approximately 4.6 million in total) that generated around 24 million edge. This project then requires predicting the probability of the directed links between the 2000 test nodes A to B.

## Important files
- **similarities.py** includes all similarity functions
- **kernel.py** includes Kernel class to run through the data and generate prediction. It is also runnable.

## How to run
- Place all data files to the data folder 
- Update GLOBAL_VARIABLES in kernel.py
- run `python kernel.py`

## Tested environment
- Python 3.6
- Ubuntu 16.04
- **Anaconda** virtual environment was used for packages

## Required Python packages
- numpy and scipy
- scikit learn
- pandas
