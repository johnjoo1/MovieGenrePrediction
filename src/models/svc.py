# non deep learning on bag of words

# load pickles and libraries
from src.utils.eval_metrics import *
from src.utils.initialize import *
from sklearn.model_selection import train_test_split
import pickle

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
with open('data/processed/X_tfidf.pkl','rb') as f:
    X=pickle.load(f)
print("Loaded X_tfidf from data/processed/X_tfidf.pkl.\n")

indecies = range(len(movies_with_overviews))
X_train, X_test, Y_train, Y_test, train_movies, test_movies = train_test_split(X, Y, indecies, test_size=0.20, random_state=42)
genre_names=list(Genre_ID_to_name.values())
print("Split X and Y into a training and test set. Split was 80-20.")
print("Shape of X_test is {X_test}.".format(X_test=X_test.shape))
print("Shape of X_train is {X_train}.\n".format(X_train=X_train.shape))

###### SVC #########
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import f1_score
from sklearn.metrics import make_scorer
from sklearn.metrics import classification_report

parameters = {'kernel':['linear'], 'C':[0.01, 0.1, 1.0]}
gridCV = GridSearchCV(SVC(class_weight='balanced'), parameters, scoring=make_scorer(f1_score, average='micro'), verbose=True)
classif = OneVsRestClassifier(gridCV)

print("Starting C-SVM training with the following parameters: {parameters}".format(parameters=parameters))
classif.fit(X_train, Y_train)

predstfidf=classif.predict(X_test)

print("Training Done!\n")
print (classification_report(Y_test, predstfidf, target_names=genre_names)) # save to file to show as a result

with open('models/classifier_svc.pkl','wb') as f:
    pickle.dump(classif,f)

####

predictions = generate_predictions(Genre_ID_to_name, X_test, predstfidf)
precs, recs = precsc_recs(test_movies, movies_with_overviews, Genre_ID_to_name, predictions)

prec_mean = np.mean(np.asarray(precs))
rec_mean = np.mean(np.asarray(recs))

print("\nMean precision between genres is {prec_mean}.".format(prec_mean=prec_mean))
print("Mean recall between genres is {rec_mean}.".format(rec_mean=rec_mean))
import json
with open('dominostats.json', 'w') as f:
    f.write(json.dumps({"Precision": prec_mean, "Recall": rec_mean}))
print("Saved metrics to dominostats.json. You should be able to see these on the Jobs Dashboard.")
