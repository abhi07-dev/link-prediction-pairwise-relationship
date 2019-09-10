How to generate data?
===============
- Update train_path vallue in generator.py
- run generator.py with python 3.6. It will create instances.txt and labels.txt
- scikit-learn package was used to implement data generator so absence of it will cause error
- features.py will read from instances.txt and by running feature generators in metrics/ creates features.csv

What is generated data?
===============
- 25000 positive and 25000 negative instances in instances.txt and labels.txt
- instances.txt format of each row: A \tab B