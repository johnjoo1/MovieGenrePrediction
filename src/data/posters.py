from src.utils.initialize import *

# the pickle should be a command line arg, with default
with open('data/interim/movies.pkl','rb') as f:
    movies=pickle.load(f)

##################
# Get posters
poster_movies=[]
counter=0
movies_no_poster=[]
print("Total movies : ",len(movies))
print("Started downloading posters...")
for movie in movies:
    id=movie['id']
    title=movie['title']
    if counter==1:
        print('Downloaded first. Code is working fine. Please wait, this will take quite some time...')
    if counter%300==0 and counter!=0:
        print( "Done with ",counter," movies!")
        print ("Trying to get poster for ",title)
    try:
        grab_poster_tmdb(title)
        poster_movies.append(movie)
    except:
        try:
            time.sleep(7)
            grab_poster_tmdb(title)
            poster_movies.append(movie)
        except:
            movies_no_poster.append(movie)
    counter+=1
print("Done with all the posters!")

###################################

with open('data/interim/poster_movies.pkl','wb') as f:
    pickle.dump(poster_movies,f)