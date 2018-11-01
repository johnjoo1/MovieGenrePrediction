import pickle
from keras.models import load_model
from sklearn.preprocessing import MultiLabelBinarizer
from gensim import models
from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
import numpy as np

with open('models/count_vectorizer.pkl','rb') as f:
    count_vectorizer=pickle.load(f)
with open('models/classifier_svc.pkl','rb') as f:
    classif_nb=pickle.load(f)
with open('models/classifier_nb.pkl','rb') as f:
    classif_svc=pickle.load(f)
with open('data/processed/Genredict.pkl','rb') as f:
    Genre_ID_to_name=pickle.load(f)
with open('models/tfidf_transformer.pkl','rb') as f:
    tfidf_transformer=pickle.load(f)
    
model_textual = load_model('models/overview_nn.h5')
w2v_model = models.KeyedVectors.load_word2vec_format('data/external/GoogleNews-vectors-negative300.bin', binary=True)
tokenizer = RegexpTokenizer(r'\w+')
en_stop = get_stop_words('en')
with open('models/mlb.pkl','rb') as f:
    mlb=pickle.load(f)

genre_list=sorted(list(Genre_ID_to_name.keys()))

def remove_punctuation(input_string):
    cleaned_string = input_string.replace(',','')
    cleaned_string = cleaned_string.replace('.','')    
    return cleaned_string
    
def nb_predict(input_string):
    cleaned_string = remove_punctuation(input_string)
    vectorized_doc = count_vectorizer.transform([cleaned_string])
    pred_array = classif_nb.predict(vectorized_doc)
    pred_prob = classif_nb.predict_proba(vectorized_doc)
    pred_genres = []
    for i, score in enumerate(pred_array[0]):
        if score!=0:
            genre=Genre_ID_to_name[genre_list[i]]
            pred_genres.append(genre)
    return pred_genres, pred_prob

def svc_predict(input_string):
    cleaned_string = remove_punctuation(input_string)
    vectorized_doc = count_vectorizer.transform([cleaned_string])
    tfidf_doc = tfidf_transformer.transform(vectorized_doc)
    pred_array = classif_svc.predict(tfidf_doc)
#     pred_prob = classif_svc.predict_proba(tfidf_doc) # trained with probability=False to save time, so not available
    pred_genres = []
    for i, score in enumerate(pred_array[0]):
        if score!=0:
            genre=Genre_ID_to_name[genre_list[i]]
            pred_genres.append(genre)
    return pred_genres #, pred_prob

def nn_predict(input_string):
    movie_mean_wordvec=np.zeros((1,300))
    tokens = tokenizer.tokenize(input_string)
    stopped_tokens = [k for k in tokens if not k in en_stop]
    count_in_vocab=0
    s=0
    for tok in stopped_tokens:
        if tok.lower() in w2v_model.vocab:
            count_in_vocab+=1
            s+=w2v_model[tok.lower()]
    if count_in_vocab!=0:
        movie_mean_wordvec[0]=s/float(count_in_vocab)
    pred_array = model_textual.predict(movie_mean_wordvec)
    predicted = np.argsort(pred_array[0])[::-1][:3]
    predicted_genre_Y = np.array([[1 if k in predicted else 0 for k in range(len(pred_array[0])) ]])
    predicted_genre_ids = mlb.inverse_transform(predicted_genre_Y)[0]
    predicted_genres = list(map(Genre_ID_to_name.get, predicted_genre_ids))
    return predicted_genres