import pickle
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras import optimizers
from sklearn.preprocessing import MultiLabelBinarizer
from src.utils.eval_metrics import *

from sklearn.model_selection import train_test_split

with open('data/processed/textual_features.pkl','rb') as f:
    (X,Y)=pickle.load(f)
with open('models/mlb.pkl','rb') as f:
    mlb=pickle.load(f)
with open('data/processed/Genredict.pkl','rb') as f:
    Genre_ID_to_name=pickle.load(f)

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.20, random_state=42)

model_textual = Sequential([
    Dense(300, input_shape=(300,)),
    Activation('relu'),
    Dense(np.shape(Y)[1]),
    Activation('softmax'),
])

model_textual.compile(optimizer='rmsprop',
              loss='binary_crossentropy',
              metrics=['accuracy'])

model_textual.fit(X_train, Y_train, epochs=5000, batch_size=500,verbose=1)

score = model_textual.evaluate(X_test, Y_test, batch_size=249)
print("%s: %.2f%%" % (model_textual.metrics_names[1], score[1]*100))
Y_preds=model_textual.predict(X_test)

model_textual.save("models/overview_nn.h5")

print ("Our predictions for the movies are - \n")
precs=[]
recs=[]
for i in range(len(Y_preds)):
    row=Y_preds[i]
    gt_genres=Y_test[i]
    gt_genre_names=[]
    genre_ids = mlb.inverse_transform(np.array([gt_genres]))[0]
    gt_genre_names = list(map(Genre_ID_to_name.get, genre_ids))
    
    prediction_criteria = 'top_3'
    prediction_threshold = 0.75
    if prediction_criteria == 'top_3':
        predicted = np.argsort(row)[::-1][:3]
        predicted_genre_Y = np.array([[1 if k in predicted else 0 for k in range(len(row)) ]])
    elif prediction_criteria == 'threshold':
        predicted_genre_Y = np.array([(row>prediction_threshold)*1])
    predicted_genre_ids = mlb.inverse_transform(predicted_genre_Y)[0]
    predicted_genres = list(map(Genre_ID_to_name.get, predicted_genre_ids))
    
    (precision,recall)=precision_recall(gt_genre_names,predicted_genres)
    precs.append(precision)
    recs.append(recall)
    if i%50==0:
        print ("Predicted: ",predicted_genres," Actual: ",gt_genre_names)

prec_mean = np.mean(np.asarray(precs))
rec_mean = np.mean(np.asarray(recs))

import json
with open('dominostats.json', 'w') as f:
    f.write(json.dumps({"Precision": prec_mean, "Recall": rec_mean}))
print("Precision: ", prec_mean)
print("Recall: ", rec_mean)   
