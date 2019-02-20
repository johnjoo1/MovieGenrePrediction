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
from src.apis.api_nb import *
import pandas as pd
    
batch_file = 'batch_overviews.txt'
results = []

with open(batch_file, "r") as f:
    for line in f:
        overview = remove_punctuation(line)
        result_list = nb_predict(overview)
        results.append([line, result_list[0], result_list[1]])
        
df = pd.DataFrame.from_records(results)
df.to_csv('results/batch_results.csv', index=False)
        

        

