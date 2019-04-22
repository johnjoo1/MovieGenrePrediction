from src.utils.initialize import *
import pprint
 
# Get the text data from top 1000 popular movies ########
all_movies=tmdb.Movies()
top_movies=all_movies.popular()
 
# TODO parameterize by making top N movies
top1000_movies=[]
print('Pulling movie list of popular movies, Please wait...')
print('\tWhile you wait, here are some sampling of the movies that are being pulled...')
for i in range(1,51):
    if i%10==0:
        print('\t' + str(i) + '/51 done')
        print('\t******* Waiting a few seconds to stay within rate limits of TMDB... *******)')
        time.sleep(7)
    movies_on_this_page=all_movies.popular(page=i)['results']
    print('\t\t'+movies_on_this_page[-1]['title'])
    top1000_movies.extend(movies_on_this_page)
len(top1000_movies)
 
print('Done! Pulled a list of the top {n} movies.'.format(n = len(top1000_movies)))
print('\n')
 
print('Extracting the genre ids associated with the movies....')
genre_ids_ = list(map(lambda x: x['genre_ids'], top1000_movies))
genre_ids_ = [item for sublist in genre_ids_ for item in sublist]
nr_ids = list(set(genre_ids_))
print('Done! We have identified {n} genres in the top {m} most popular movies.'.format(n=len(nr_ids), m=len(top1000_movies)))
print('\n')
 
##############################
# Get poster data from another sample of movies from the genres listed in the top 1000 movies for a specific year #################
# Done before, reading from pickle file now to maintain consistency of data!
# We now sample 100 movies per genre. Problem is that the sorting is by popular movies, so they will overlap.
# In other words, popular movies may be in more than 1 genre.
# Need to exclude movies that were already sampled. 
movies = []
baseyear = 2017
 
print('Starting pulling movies from TMDB from each genre. This will take a while, please wait...')
done_ids=[]
for g_id in nr_ids:
    print('\tPulling movies for genre ID {g_id}. Here are sample of movies in the genre: '.format(g_id = str(g_id)) )
    baseyear -= 1
    for page in range(1,6,1): # (1,6,1)
        time.sleep(1)
    
        url = 'https://api.themoviedb.org/3/discover/movie?api_key=' + api_key
        url += '&language=en-US&sort_by=popularity.desc&year=' + str(baseyear) 
        url += '&with_genres=' + str(g_id) + '&page=' + str(page)
 
        data = urllib.request.urlopen(url).read()
 
        dataDict = json.loads(data)
        movies.extend(dataDict["results"])
    last_movies = list(map(lambda x: x['title'],movies[-3:]))
    for title in last_movies:
        print('\t\t'+title)
    done_ids.append(str(g_id))
print("\tPulled movies for genres - "+','.join(done_ids))
print('\n')
 
# Remove duplicates
movie_ids = [m['id'] for m in movies]
print ("Originally we had ",len(movie_ids)," movies")
movie_ids=np.unique(movie_ids)
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
print('\n')

print("Saving the list of de-duped list of movies (no_duplicate_movies) as data/interim/no_duplicate_movies.pkl...")
print('\tHere are the first 3 entries in no_duplicate_movies:')
pprint.pprint(no_duplicate_movies[:3], indent=4)
with open('data/interim/no_duplicate_movies.pkl', 'wb') as f:
    pickle.dump(no_duplicate_movies, f)
print("Saved the list of de-duped list of movies as data/interim/no_duplicate_movies.pkl.")    



## TODO include a dominostats.json
