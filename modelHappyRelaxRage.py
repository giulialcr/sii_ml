# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 20:16:44 2019

@author: Giulia
"""

import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.optimizers import SGD
from keras.utils import to_categorical, normalize
from os import sep # Il separatore per i path nel sistema operativo corrente 
import readmatrix as rdmt


import pandas

from keras.wrappers.scikit_learn import KerasClassifier
from keras.utils import np_utils
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline

# Carica i dati e crea il dataset
import numpy as np

# fix random seed for reproducibility
seed = 7
np.random.seed(seed)


# Lettura da file a matrice
mat_rage= rdmt.to_matrix('data' + sep + 'rage.txt', 0, 800)
mat_relax = rdmt.to_matrix('data' + sep + 'relax.txt', 1, 800)
mat_happy = rdmt.to_matrix('data' + sep + 'happy.txt', 2, 800)
dataset1 = np.append(mat_rage, mat_relax, axis=0)
dataset=np.append(mat_happy,dataset1, axis=0)


np.random.shuffle(dataset)
np.unique(dataset)
# Dimensioni test set (20% dataset)
tsize = (np.size(dataset, 0) * 20) // 100
print(f"Test set size: {tsize}")
input("Premi qualsiasi tasto per continuare, Ctr+C per terminare.")

training = dataset[:-tsize]

test = dataset[-tsize:]

# Model
model = Sequential()



# Compile model

model.add(Dense(20, activation='relu', input_dim=10))
#model.add(Dropout(0.3))
model.add(Dense(16, activation='relu'))
#model.add(Dropout(0.3))
model.add(Dense(8, activation='relu'))
#model.add(Dropout(0.3))
model.add(Dense(3, activation='softmax'))

model.summary()

sgd = SGD(lr=0.5)
model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

# Training:
# training[...,:-1] prende i valori esclusa la colonna delle labels
# normalizzo i valori prima dell'addestramento
x_train = normalize(training[...,:-1], axis=1, order=1)
y_train = to_categorical(training[...,-1])

model.fit(x_train, y_train,
          epochs=200,
          verbose=1,
          batch_size=5)

#Testing
x_test = normalize(test[...,:-1], axis=1, order=1)
y_test = to_categorical(test[...,-1])

score = model.evaluate(x_test, y_test, batch_size=1)
print(score)

print()
while True:
    save = input("Salvare il modello? y/n > ")
    if save == 'y':
        model_name = input('Inserisci il nome >>> ')
        model.save(f'models' + sep + '{model_name}.h5')
        break
    elif save == 'n':
        break

# Con questa configurazione ottenuto 0.92 di accuratezza
# Da provare: mini-batch di 5-10 canzoni
# Aumentare le dimensioni del testset
# Varie ed eventuali