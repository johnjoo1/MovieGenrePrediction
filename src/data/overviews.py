from src.utils.initialize import *
import pprint

# load no_duplicate_movies
print("Loading the list of de-duped movies from data/interim/no_duplicate_movies.pkl...")
with open('data/interim/no_duplicate_movies.pkl','rb') as f:
    no_duplicate_movies=pickle.load(f)
print("Loaded the list of de-duped movies from data/interim/no_duplicate_movies.pkl.\n")

# get movies with overviews
print("Creating a dataset where each movie must have an associated overview...")
movies_with_overviews=[] # from poster data
for i in range(len(no_duplicate_movies)):
    movie=no_duplicate_movies[i]
    id=movie['id']
    overview=movie['overview']
    
    if len(overview)==0:
        continue
    else:
        movies_with_overviews.append(movie)
print("Done! Created a dataset where each movie must have an associated overview.\n")
len(movies_with_overviews)


print("Saving the list of movies that have overviews (movies_with_overviews) as data/interim/movies_with_overviews.pkl....")
print('\tHere are the first entry in movies_with_overviews:')
pprint.pprint(movies_with_overviews[0], indent=4)
with open('data/interim/movies_with_overviews.pkl','wb') as f:
    pickle.dump(movies_with_overviews,f)
print("Saved the list of movies that have overviews (movies_with_overviews) as data/interim/movies_with_overviews.pkl.")