import pickle
import numpy as np
from sklearn.preprocessing import MultiLabelBinarizer
from src.utils.eval_metrics import *
import os

from sklearn.model_selection import train_test_split

with open('data/processed/movies_with_overviews.pkl','rb') as f:
    final_movies_set=pickle.load(f)


from gensim import models
model2 = models.KeyedVectors.load_word2vec_format('data/external/GoogleNews-vectors-negative300.bin', binary=True)


from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
tokenizer = RegexpTokenizer(r'\w+')

# create English stop words list
en_stop = get_stop_words('en')


movie_mean_wordvec=np.zeros((len(final_movies_set),300))


genres=[]
rows_to_delete=[]
for i in range(len(final_movies_set)):
    mov=final_movies_set[i]
    movie_genres=mov['genre_ids']
    genres.append(movie_genres)
    overview=mov['overview']
    tokens = tokenizer.tokenize(overview)
    stopped_tokens = [k for k in tokens if not k in en_stop]
    count_in_vocab=0
    s=0
    if len(stopped_tokens)==0:
        rows_to_delete.append(i)
        genres.pop(-1)
#         print overview
#         print "sample ",i,"had no nonstops"
    else:
        for tok in stopped_tokens:
            if tok.lower() in model2.vocab:
                count_in_vocab+=1
                s+=model2[tok.lower()]
        if count_in_vocab!=0:
            movie_mean_wordvec[i]=s/float(count_in_vocab)
        else:
            rows_to_delete.append(i)
            genres.pop(-1)
#             print overview
#             print "sample ",i,"had no word2vec"

mask2=[]
for row in range(len(movie_mean_wordvec)):
    if row in rows_to_delete:
        mask2.append(False)
    else:
        mask2.append(True)
        
X=movie_mean_wordvec[mask2]

mlb=MultiLabelBinarizer()
Y=mlb.fit_transform(genres)

textual_features=(X,Y)
with open('data/processed/textual_features.pkl','wb') as f:
    pickle.dump(textual_features,f)
with open('models/mlb.pkl','wb') as f:
    pickle.dump(mlb,f)

os.remove("data/external/GoogleNews-vectors-negative300.bin")
