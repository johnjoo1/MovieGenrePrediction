# non deep learning on bag of words

# load pickles and libraries
from src.utils.eval_metrics import *
from src.utils.initialize import *
from sklearn.model_selection import train_test_split

with open('data/interim/movies_with_overviews.pkl','rb') as f:
    movies_with_overviews=pickle.load(f)
with open('data/processed/Genredict.pkl','rb') as f:
    Genre_ID_to_name=pickle.load(f)  
with open('data/processed/Y.pkl','rb') as f:
    Y=pickle.load(f)
print("Loaded the list of de-duped movies with overviews from data/interim/movies_with_overviews.pkl.")
print('Loaded the mapping from genre id to genre name from data/processed/Genredict.pkl.')
print("Loaded the target variable Y from data/processed/Y.pkl.")

    
# Feature Selection and Test/Train Split

with open('data/processed/X.pkl','rb') as f:
    X=pickle.load(f)
print("Loaded X from data/processed/X.pkl.\n")


indecies = range(len(movies_with_overviews))
X_train, X_test, Y_train, Y_test, train_movies, test_movies = train_test_split(X, Y, indecies, test_size=0.20, random_state=42)
print("Split X and Y into a training and test set. Split was 80-20.")
print("Shape of X_test is {X_test}.".format(X_test=X_test.shape))
print("Shape of X_train is {X_train}.\n".format(X_train=X_train.shape))


genre_names=list(Genre_ID_to_name.values())

###### Naive Bayes ########
from sklearn.multiclass import OneVsRestClassifier
from sklearn.metrics import f1_score
from sklearn.metrics import make_scorer
from sklearn.metrics import classification_report
from sklearn.naive_bayes import MultinomialNB

classifnb = OneVsRestClassifier(MultinomialNB())
classifnb.fit(X_train, Y_train)
predsnb=classifnb.predict(X_test)
print("Trained using Multinomial Naive Bayes.")

print (classification_report(Y_test, predsnb, target_names=genre_names)) # save to file to show as a result

import pickle
f2=open('models/classifier_nb.pkl','wb')
pickle.dump(classifnb,f2)
f2.close()


##########

predictionsnb = generate_predictions(Genre_ID_to_name, X_test, predsnb)
precs, recs = precsc_recs(test_movies, movies_with_overviews, Genre_ID_to_name, predictionsnb)

prec_mean = np.mean(np.asarray(precs))
rec_mean = np.mean(np.asarray(recs))

print("\nMean precision between genres is {prec_mean}.".format(prec_mean=prec_mean))
print("Mean recall between genres is {rec_mean}.".format(rec_mean=rec_mean))
import json
with open('dominostats.json', 'w') as f:
    f.write(json.dumps({"Precision": prec_mean, "Recall": rec_mean}))
print("Saved metrics to dominostats.json. You should be able to see these on the Jobs Dashboard.")
    
