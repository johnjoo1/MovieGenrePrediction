from src.utils.initialize import *
import re


with open('data/processed/Y.pkl','rb') as f:
    Y=pickle.load(f)
with open('data/processed/movies_with_overviews.pkl','rb') as f:
    movies_with_overviews=pickle.load(f)
with open('data/processed/Genredict.pkl','rb') as f:
    Genre_ID_to_name=pickle.load(f)    
    
genre_names=list(Genre_ID_to_name.values())

# remove some punctuation
def remove_punctuation(input_string):
    input_string = input_string.replace(',','')
    cleaned_string = input_string.replace('.','')    
    return cleaned_string

content=[]
for i in range(len(movies_with_overviews)):
    movie=movies_with_overviews[i]
    id=movie['id']
    overview=movie['overview']
    overview=remove_punctuation(overview)
    content.append(overview)


# Count Vectorize
from sklearn.feature_extraction.text import CountVectorizer
vectorize=CountVectorizer(max_df=0.95, min_df=0.005)
X=vectorize.fit_transform(content)
print("Shape of X with count vectorizer:")
print(X.shape)
with open('data/processed/X.pkl','wb') as f:
    pickle.dump(X,f)
with open('models/count_vectorizer.pkl','wb') as f:
    pickle.dump(vectorize,f)

# TF-IDF
from sklearn.feature_extraction.text import TfidfTransformer
tfidf_transformer = TfidfTransformer()
X_tfidf = tfidf_transformer.fit_transform(X)
print("Shape of X_tfidf:")
print(X_tfidf.shape)
with open('data/processed/X_tfidf.pkl','wb') as f:
    pickle.dump(X_tfidf,f)
with open('models/tfidf_transformer.pkl','wb') as f:
    pickle.dump(tfidf_transformer,f)


