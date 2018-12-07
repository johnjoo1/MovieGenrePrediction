import pickle

with open('models/count_vectorizer.pkl','rb') as f:
    count_vectorizer=pickle.load(f)
with open('models/classifier_svc.pkl','rb') as f:
    classif_svc=pickle.load(f)
with open('data/processed/Genredict.pkl','rb') as f:
    Genre_ID_to_name=pickle.load(f)
with open('models/tfidf_transformer.pkl','rb') as f:
    tfidf_transformer=pickle.load(f)

genre_list=sorted(list(Genre_ID_to_name.keys()))

def remove_punctuation(input_string):
    cleaned_string = input_string.replace(',','')
    cleaned_string = cleaned_string.replace('.','')    
    return cleaned_string

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

