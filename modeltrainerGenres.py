# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 23:21:01 2019

"""

import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.optimizers import SGD
from keras.utils import to_categorical, normalize
from os import sep # Il separatore per i path nel sistema operativo corrente 
import readmatrix as rdmt

# Carica i dati e crea il dataset
import numpy as np
# Lettura da file a matrice
mat_dance = rdmt.to_matrix('data' + sep + 'dance.txt', 0, 600)
mat_rock = rdmt.to_matrix('data' + sep + 'rock.txt', 1, 600)
mat_classical= rdmt.to_matrix('data' + sep + 'classical.txt', 2, 600)
mat_blues = rdmt.to_matrix('data' + sep + 'blues.txt', 3, 600)
dataset1 = np.append(mat_rock, mat_dance, axis=0)
dataset2=np.append(mat_classical, mat_blues, axis=0)
dataset=np.append(dataset1,dataset2, axis=0)
#FIN QUI
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

model.add(Dense(32, activation='relu', input_dim=10))
#model.add(Dropout(0.3))
model.add(Dense(16, activation='relu'))
#model.add(Dropout(0.3))
model.add(Dense(8, activation='relu'))
#model.add(Dropout(0.3))
model.add(Dense(4, activation='softmax'))
#model.add(Dense(2, activation='softmax'))

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
          epochs=2000,
          verbose=1,
          batch_size=10)

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

# Con questa configurazione ottenuto 0.87 di accuratezza
# Da provare: mini-batch di 5-10 canzoni
# Aumentare le dimensioni del testset
# Varie ed eventuali
