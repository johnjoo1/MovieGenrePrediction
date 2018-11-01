import pickle
from sklearn.preprocessing import MultiLabelBinarizer
import numpy as np
from sklearn.model_selection import train_test_split
from src.utils.eval_metrics import *

from keras.models import Sequential
from keras.layers import Dense, Activation
from keras import optimizers

with open('data/processed/posters_new_features.pkl','rb') as f:
    list_pickled=pickle.load(f)
with open('data/processed/Genredict.pkl','rb') as f:
    Genre_ID_to_name=pickle.load(f) 

(feature_list,files,failed,succesful,genre_list)=list_pickled

(a,b,c,d)=feature_list[0].shape
feature_size=a*b*c*d
np_features=np.zeros((len(feature_list),feature_size))

for i in range(len(feature_list)):
    feat=feature_list[i]
    reshaped_feat=feat.reshape(1,-1)
    np_features[i]=reshaped_feat

X=np_features

mlb=MultiLabelBinarizer()
Y=mlb.fit_transform(genre_list)

visual_problem_data=(X,Y)
with open('data/processed/visual_problem_data_clean.pkl','wb') as f:
    pickle.dump(visual_problem_data,f)

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.20, random_state=42)



model_visual = Sequential([
    Dense(1024, input_shape=(25088,)),
    Activation('relu'),
    Dense(256),
    Activation('relu'),
    Dense(np.shape(Y)[1]),
    Activation('sigmoid'),
])
opt = optimizers.rmsprop(lr=0.0001, decay=1e-6)

#sgd = optimizers.SGD(lr=0.05, decay=1e-6, momentum=0.4, nesterov=False)
model_visual.compile(optimizer=opt,
              loss='binary_crossentropy',
              metrics=['accuracy'])

model_visual.fit(X_train, Y_train, epochs=20, batch_size=64,verbose=1)

Y_preds=model_visual.predict(X_test)

model_visual.save("models/poster_nn.h5")



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
        print ("Predicted: ",','.join(predicted_genres)," Actual: ",','.join(gt_genre_names))
        
prec_mean = np.mean(np.asarray(precs))
rec_mean = np.mean(np.asarray(recs))

import json
with open('dominostats.json', 'w') as f:
    f.write(json.dumps({"Precision": prec_mean, "Recall": rec_mean}))
print("Precision: ", prec_mean)
print("Recall: ", rec_mean)