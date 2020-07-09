import pickle
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras import optimizers
from sklearn.preprocessing import MultiLabelBinarizer
from src.utils.eval_metrics import *
import time

from sklearn.model_selection import train_test_split

with open('data/processed/textual_features.pkl','rb') as f:
    (X,Y)=pickle.load(f)
with open('models/mlb.pkl','rb') as f:
    mlb=pickle.load(f)
with open('data/processed/Genredict.pkl','rb') as f:
    Genre_ID_to_name=pickle.load(f)
print("Loaded X and Y from data/processed/textual_features.pkl.")
print('Loaded the mapping from genre id to genre name from data/processed/Genredict.pkl.')
print("Loaded the multi-label binarizer as models/mlb.pkl so we can do the inverse transform.")
    

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.20, random_state=42)
print("\nSplit X and Y into a training and test set. Split was 80-20.")
print("\tShape of X_test is {X_test}.".format(X_test=X_test.shape))
print("\tShape of X_train is {X_train}.\n".format(X_train=X_train.shape))



model_textual = Sequential([
    Dense(300, input_shape=(300,)),
    Activation('relu'),
    Dense(np.shape(Y)[1]),
    Activation('softmax'),
])

model_textual.compile(optimizer='rmsprop',
              loss='binary_crossentropy',
              metrics=['accuracy'])

## needs apt-get install graphiz && pip install pydot
# from keras.utils import plot_model
# plot_model(model_textual, to_file='models/nn_figs/model.png', show_shapes=True)
# print("Saved visualization of model architecture to models/nn_figs/model.png.")

print("Starting training...")
history = model_textual.fit(X_train, Y_train, epochs=5000, batch_size=500,verbose=1) #5000
print("Training done!\n")

###
import matplotlib.pyplot as plt

# Plot training & validation accuracy values
plt.plot(history.history['accuracy'])
plt.title('Model accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.savefig('models/nn_figs/nn_training_validation_accuracy.png')

# Plot training & validation loss values
plt.clf()
plt.plot(history.history['loss'])
plt.title('Model loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.savefig('models/nn_figs/nn_training_validation_loss.png')

print("Saved training history visualization to models/nn_figs/nn_training_validation_accuracy.png and models/nn_figs/nn_training_validation_loss.png.\n")
###

score = model_textual.evaluate(X_test, Y_test, batch_size=249)
# print("%s: %.2f%%" % (model_textual.metrics_names[1], score[1]*100))
Y_preds=model_textual.predict(X_test)

model_textual.save("models/overview_nn.h5")
print("Saved the model to models/overview_nn.h5.\n")

print ("Our predictions vs actual for a sample of movies: ")
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
        print ("\tPredicted: ",predicted_genres," \tActual: ",gt_genre_names)

prec_mean = np.mean(np.asarray(precs))
rec_mean = np.mean(np.asarray(recs))

print("\nMean precision between genres is {prec_mean}.".format(prec_mean=prec_mean))
print("Mean recall between genres is {rec_mean}.".format(rec_mean=rec_mean))
import json
with open('dominostats.json', 'w') as f:
    f.write(json.dumps({"Precision": prec_mean, "Recall": rec_mean}))
print("Saved metrics to dominostats.json. You should be able to see these on the Jobs Dashboard.")
