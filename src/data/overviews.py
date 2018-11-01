from src.utils.initialize import *

# build dataset 

# cleaning

# load no_duplicate_movies
with open('data/interim/no_duplicate_movies.pkl','rb') as f:
    no_duplicate_movies=pickle.load(f)

# get movies with overviews
movies_with_overviews=[] # from poster data
for i in range(len(no_duplicate_movies)):
    movie=no_duplicate_movies[i]
    id=movie['id']
    overview=movie['overview']
    
    if len(overview)==0:
        continue
    else:
        movies_with_overviews.append(movie)
        
len(movies_with_overviews)

with open('data/interim/movies_with_overviews.pkl','wb') as f:
    pickle.dump(movies_with_overviews,f)