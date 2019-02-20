'''
    Command Line Args:
        file: str
            This is the name of the file that is uploaded. 
            When using with a Launcher, the Launcher will automatically complete 
            this with the path of the uploaded file.

    Returns:
        scores.json
'''
import pickle
from src.apis.api_nn import *
import os
import pandas as pd
    
batch_file = 'batch_overviews.txt'
results = []

with open(batch_file, "r") as f:
    for line in f:
        overview = line
        result_list = nn_predict(overview)
        results.append([line, result_list])
        
df = pd.DataFrame.from_records(results)
df.to_csv('results/batch_results.csv', index=False)                        

os.remove("data/external/GoogleNews-vectors-negative300-SLIM.bin")

        

