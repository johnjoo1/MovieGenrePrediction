import pickle

with open('models/count_vectorizer.pkl','rb') as f:
    count_vectorizer=pickle.load(f)
with open('models/classifier_nb.pkl','rb') as f:
    classif_nb=pickle.load(f)
with open('data/processed/Genredict.pkl','rb') as f:
    Genre_ID_to_name=pickle.load(f)



genre_list=sorted(list(Genre_ID_to_name.keys()))

def remove_punctuation(input_string):
    cleaned_string = input_string.replace(',','')
    cleaned_string = cleaned_string.replace('.','')    
    return cleaned_string
    
def nb_predict(input_string):
    cleaned_string = remove_punctuation(input_string)
    vectorized_doc = count_vectorizer.transform([cleaned_string])
    pred_array = classif_nb.predict(vectorized_doc)
    pred_prob_all = classif_nb.predict_proba(vectorized_doc)
    pred_genres = []
    pred_prob_return = []
    for i, score in enumerate(pred_array[0]):
        if score!=0:
            genre=Genre_ID_to_name[genre_list[i]]
            pred_genres.append(genre)
            pred_prob_return.append(pred_prob_all[0][i])
    return [pred_genres, pred_prob_return]