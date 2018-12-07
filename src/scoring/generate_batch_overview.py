from src.utils.initialize import *
 
# Get the text data from top 1000 popular movies ########
all_movies=tmdb.Movies()
top_movies=all_movies.popular()
 
# TODO parameterize by making top N movies
all_movies=tmdb.Movies()
top1000_movies=[]
print('Pulling movie list, Please wait...')
for i in range(1,51):
    if i%15==0:
        time.sleep(7)
    movies_on_this_page=all_movies.popular(page=i)['results']
    top1000_movies.extend(movies_on_this_page)
len(top1000_movies)
 
print('Done!')
 
 
genre_ids_ = list(map(lambda x: x['genre_ids'], top1000_movies))
genre_ids_ = [item for sublist in genre_ids_ for item in sublist]
nr_ids = list(set(genre_ids_))
 
 
##############################
# Get poster data from another sample of movies from the genres listed in the top 1000 movies for a specific year #################
# Done before, reading from pickle file now to maintain consistency of data!
# We now sample 100 movies per genre. Problem is that the sorting is by popular movies, so they will overlap.
# In other words, popular movies may be in more than 1 genre.
# Need to exclude movies that were already sampled. 
movies = []
baseyear = 2017
 
print('Starting pulling movies from TMDB. This will take a while, please wait...')
done_ids=[]
for g_id in nr_ids:
    print('Pulling movies for genre ID '+str(g_id))
    baseyear -= 1
    for page in range(1,6,1): # (1,6,1)
        time.sleep(0.5)
    
        url = 'https://api.themoviedb.org/3/discover/movie?api_key=' + api_key
        url += '&language=en-US&sort_by=popularity.desc&year=' + str(baseyear) 
        url += '&with_genres=' + str(g_id) + '&page=' + str(page)
 
        data = urllib.request.urlopen(url).read()
 
        dataDict = json.loads(data)
        movies.extend(dataDict["results"])
    done_ids.append(str(g_id))
print("Pulled movies for genres - "+','.join(done_ids))
 
# Remove duplicates
movie_ids = [m['id'] for m in movies]
print ("originally we had ",len(movie_ids)," movies")
movie_ids=np.unique(movie_ids)
print (len(movie_ids))
seen_before=[]
no_duplicate_movies=[]
for i in range(len(movies)):
    movie=movies[i]
    id=movie['id']
    if id in seen_before:
        continue
        print ("Seen before")
    else:
        seen_before.append(id)
        no_duplicate_movies.append(movie)
        
print ("After removing duplicates we have ",len(no_duplicate_movies), " movies")
 
movies_with_overviews=[] # from poster data
for i in range(len(no_duplicate_movies)):
    movie=no_duplicate_movies[i]
    id=movie['id']
    overview=movie['overview']
    
    if len(overview)==0:
        continue
    else:
        movies_with_overviews.append(movie)
        
overviews = [x['overview'] for x in movies_with_overviews]

for overview in overviews:
    with open("batch_overviews.txt", "a+") as f:
        f.write(overview)
        f.write('\n')