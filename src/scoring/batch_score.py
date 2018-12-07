'''
    Command Line Args:
        model_type: str 
            Possible arguments are `nb` for Naive Bayes, 
                                   `svc` for C-Support Vector Classification, and 
                                   `nn` for a neural network.
        file: str
            This is the name of the file that is uploaded. 
            When using with a Launcher, the Launcher will automatically complete 
            this with the path of the uploaded file.

    Returns:
        File: results/batch_results.csv
'''
import sys
import pickle
import pandas as pd
import os
    
args = sys.argv
model_type = args[1]
if args[2]:
    batch_file = args[2]
else:
    batch_file = 'batch_overviews.txt'

results = []

if model_type == 'nb':
    from src.apis.api_nb import *
    with open(batch_file, "r") as f:
        for line in f:
            overview = remove_punctuation(line)
            result_list = nb_predict(overview)
            results.append([line, result_list[0], result_list[1]])
elif model_type == 'svc':
    from src.apis.api_svc import *
    with open(batch_file, "r") as f:
        for line in f:
            overview = remove_punctuation(line)
            result_list = svc_predict(overview)
            results.append([line, result_list])
elif model_type == 'nn':
    from src.apis.api_nn import *
    with open(batch_file, "r") as f:
        for line in f:
            overview = line
            result_list = nn_predict(overview)
            results.append([line, result_list])
    os.remove("data/external/GoogleNews-vectors-negative300.bin")

df = pd.DataFrame.from_records(results)
df.to_csv('results/batch_results.csv', index=False)
