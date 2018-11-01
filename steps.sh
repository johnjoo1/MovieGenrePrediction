python src/data/movie_list.py # 2 mins 4sec
# data/interim/movie_list.pkl
# data/interim/no_duplicate_movies.pkl
# data/interim/movies.pkl

# requires: 
#  data/interim/no_duplicate_movies.pkl
python src/data/overviews.py #1.6sec
# creates 
#  data/interim/movies_with_overviews.pkl


# requires:
#  data/interim/movies.pkl
# python src/data/posters.py
# creates:
#  data/raw/posters
#  data/interim/poster_movies.pkl


# requires:
#  data/interim/no_duplicate_movies.pkl
#  data/interim/movies_with_overviews.pkl
python src/data/cleaning_data.py #2.2sec
# creates
#  data/processed/Y.pkl
#  data/processed/Genredict.pkl
#  data/processed/movies_with_overviews.pkl

# requires:
#  data/processed/Y.pkl
#  data/processed/movies_with_overviews.pkl
#  data/processed/Genredict.pkl
python src/features/feature_eng.py # 2s
# creates:
#  data/processed/X.pkl
#  models/count_vectorizer.pkl
#  data/processed/X_tfidf.pkl
#  models/tfidf_transformer.pkl



# requires:
#  data/processed/movies_with_overviews.pkl
#  data/processed/Genredict.pkl
#  data/processed/Y.pkl
#  data/processed/X_tfidf.pkl
python src/models/svc.py #1min 43sec
# creates:
#  models/classifier_svc.pkl
  
# requires:
#  data/processed/movies_with_overviews.pkl
#  data/processed/Genredict.pkl
#  data/processed/Y.pkl
#  data/processed/X.pkl
python src/models/naive_bayes.py #1.8sec
# creates:
#  models/classifier_nb.pkl

# python src/features/image_features.py
# python src/models/poster_nn.py

sh src/models/get_word2vec.sh
# creates:
#  data/external/GoogleNews-vectors-negative300.bin

# requires:
#  data/processed/movies_with_overviews.pkl
#  data/processed/Genredict.pkl
#  data/external/GoogleNews-vectors-negative300.bin
python src/features/word2vec_features.py #52sec
# creates:
#  data/processed/textual_features.pkl
#  models/mlb.pkl

# requires:
#  data/processed/textual_features.pkl
#  models/mlb.pkl
python src/models/overview_nn.py #1min42sec
# creates:
#  models/overview_nn.h5