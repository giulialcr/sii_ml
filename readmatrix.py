import numpy as np

# Converte il file in una matrice numpy: [[<audio features>, <label>]]
def to_matrix(input_file, label, lines_to_read=-1):
    with open(input_file) as file:
        line_counter = 0
        matrix = []
        for line in file:
            if line_counter == lines_to_read:
                break
            line_counter += 1
            # Da stringa a lista
            audio_features = eval(line[:-23])
            audio_features.append(label)
            matrix.append(audio_features)

    return np.array(matrix, dtype='float32')

# test
if __name__ == '__main__':
    happy_matrix = to_matrix('happyness.txt', 0, 600)
    print("Elementi totali:", np.size(happy_matrix))
    print("Numero di righe:", np.size(happy_matrix, 0))
    print("Numero di colonne:", np.size(happy_matrix, 1))
    print(np.around(happy_matrix, decimals=0))
    
    print(happy_matrix[0,0])
    sad_matrix = to_matrix('sadness.txt', 1, 600)
    print("Elementi totali:", np.size(sad_matrix))
    print("Numero di righe:", np.size(sad_matrix, 0))
    print("Numero di colonne:", np.size(sad_matrix, 1))
    print(np.around(sad_matrix, decimals=0))

    print("\nAttacca la matrice sad in fondo alla matrice happy..\n")

    data = np.append(happy_matrix, sad_matrix, axis=0)
    np.random.shuffle(data)
    np.unique(data)
    print("Elementi totali:", np.size(data))
    print("Numero di righe:", np.size(data, 0))
    print("Numero di colonne:", np.size(data, 1))
    print("Matrice sana:\n")
    print(np.around(data, decimals=0))
    print("\nUltime tre righe di matrice (test set):")    
    print(np.around(data, decimals=0)[-3:])
    print("\nSolo dati senza labels:")
    print(np.around(data, decimals=0)[...,0:-1])
    print("\nSolo labels:")
    print(np.around(data, decimals=0)[...,-1])

    from keras.utils import to_categorical, normalize

    print(to_categorical(data[...,-1]))
    print(to_categorical(data[...,-1:]))
    print('\n\n')
    rnd = np.random.rand(5,5)
    print(rnd)
    print("Normalizzata:")
    print(normalize(rnd, axis=1, order=1))

    # La sintassi dovrebbe essere arr[riga,colonna:riga,colonna:riga,colonna]
    # i ... stanno per tutti i valori su quella riga/colonna
    # le posizioni sono arr[start:stop:step]







