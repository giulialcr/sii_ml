import os # Funzioni per il sistema operativo, qui viene usato solo per rimuovere un file
from sys import argv # Passa lo username come argomento quando viene eseguito lo script
import json # Gestione e stampa per i file json ottenuti come risposta
import spotipy # Vabbè ce lo sai
#import webbrowser
import spotipy.util as sputil # Utility per l'accesso a spotify
#from json.decoder import JSONDecodeError

# Ottieni lo username dal terminale
#username = argv[1]
username='xygmg4xlqx8s9rmmckq005xvj'


#labels
['happyness',
'sadness',
'rage',
'relax']


# NOTA: - Come ottenere lo username -
# Tramite app spotify, click su Nome Cognome in alto a destra,
# click su puntini di sospensione sotto al Nome Cognome,
# click su condividi, poi su "Copia link profilo", si ottiene:
# https://open.spotify.com/user/12345678900?si=rrQZQmP9R666IBK6CubA6Q
# lo username sono i numeri 12345678900
# >>>>> OPPURE <<<<<<<
# Accedendo al profilo sul sito spotify
# click su "imposta password del dispositivo"
# ed usare lo username del tuo dispositivo mostrato

# Cancella la cache e chiedi il permesso dell'utente
def grant_access():
    return sputil.prompt_for_user_token(username, 
                                        scope="user-read-recently-played user-read-currently-playing", 
                                        client_id = '3250eeeeca9c47ae8edca0d5bac86a92',
                                        client_secret = 'e70ae239ab604d9ba3ae02d6e4e617c0',
                                        redirect_uri="http://google.it")

try:
    token = grant_access()
except:
    os.remove(f".cache-{username}")
    token = grant_access()

# Si apre il browser che richiede le autorizzazioni una volta accettate si verra reindirizzati al sito di google
# Copiare ed incollare l'URI dal browser nella console per completare l'autorizzazione
# Se l'accesso avviene correttamente verrà creato un file di cache per l'utente che si è loggato
# Nelle esecuzioni successive se il file resta genererebbe una eccezione

# Creazione dell'oggetto Spotify
spobject = spotipy.Spotify(auth=token)

# Oggetto utente
user = spobject.current_user()

#print(spobject._get('me/player/currently-playing')["item"])






def write_tracks(text_file, tracks):
    with open(text_file, 'a+',encoding="utf-8") as file_out:
        while True:
            for item in tracks['items']:
                if 'track' in item:
                    track = item['track']
                else:
                    track = item
                try:
                    track_name= track['name']
                    track_id = track['id']
                    track_analyzed=analysis_track(track_id)
                    #file_out.write(track_id+' '+str(track_analyzed)+' '+track_name+ '\n')
                    file_out.write(str(track_analyzed)+' '+track_id+ '\n')
                except KeyError:
                    print(u'Skipping track {0} by {1} (local only?)'.format(track['name'], track['artists'][0]['name']))
            # 1 page = 50 results
            # check if there are more pages
            if tracks['next']:
                tracks = spobject.next(tracks)
            else:
                break

def write_playlist(text_name,username, playlist_id):
    results = spobject.user_playlist(username, playlist_id,fields='tracks,next,name')
    text_file=text_name+'.txt'
    #text_file = u'{0}.txt'.format(results['name'], ok='-_()[]{}')
    print(u'Writing {0} tracks to {1}'.format(results['tracks']['total'], text_file))
    tracks = results['tracks']
    write_tracks(text_file, tracks)

def analysis_track(track_id):
     audio_features = spobject.audio_features(track_id)
        
     afv = []
     vettore_features=['danceability','energy','key','loudness','speechiness','acousticness',
                       'instrumentalness','liveness','valence','tempo']
     for ft in vettore_features:
         afv.append(audio_features[0][ft])
 
     return afv
    








# Informazioni utente
displayName = user["display_name"]
nfollowers = user["followers"]["total"]

# Comincia un loop interattivo
while True:
    print()
    print(">>> Welcome to Spotify", displayName + "!")
    print(">>> Hai:", str(nfollowers), "followers.")
    print()
    print("0 - Esci.")
    print("1 - Cerca artista.")
    print("2 - Mostra ultimi brani ascoltati.")
    print("3 - Cerca playlist.")
    print()
    scelta = input("Cosa vuoi fare? ")

    # Esci dal programma
    if scelta == "0":
        print("Ciaone!")
        break

    # Ricerca artista
    if scelta == "1":
        print()
        richiesta = input("Ok, chi vuoi cercare?: ")
        print()

        # Ottieni risultati
        sresult = spobject.search(richiesta, 1, 0, 'artist')
        print(json.dumps(sresult, sort_keys=True, indent=4))

    # Mostra gli ultimi brani ascoltati
    if scelta == "2":
        print()
        # Fix: current_user_recently_played() sembra non funzionare
        # ho usato questo workaround per ottenere lo stesso risultato
        rplayed = spobject._get('me/player/recently-played', limit=20)["items"] 
        # Per ciascun item nella lista stampo informazioni
        for item in rplayed:
            print(item["played_at"], item["track"]["name"])
        #print(json.dumps(rplayed, sort_keys=True, indent=4))

    # Ricerca playlist
    if scelta == "3":
        print()
        
        print()
        list_mood=['happyness','sadness','rage','relax'] 
        for i, m in enumerate(list_mood):
            print(i, '-', m)
        print()
        mood_text = input("Ok, che mood vuoi analizzare? ")
        text_name=list_mood[int(mood_text)]
        richiesta = input("Ok, nome playlist?: ")
        print()

        # Ottieni risultati
        limit=10
        sresult = spobject.search(richiesta, limit, 0, 'playlist')
        #print(json.dumps(sresult, sort_keys=True, indent=3))
        
        # Ottengo la lista di risultati come lista di dict playlist
        lista_playlist = sresult['playlists']['items']

        for i, playlist in enumerate(lista_playlist):
            print(f'{i}. ' + playlist['name'] + ', Total tracks: ' + str(playlist['tracks']['total']) + ' ' + playlist['id'])
        
        i=0
        while i<limit:
            print('\n se vuoi tornare al menu principale inserisci q')
            num = input('\nInserisci un numero per vedere l analisi della playlist oppure q per uscire: ')
            if num != 'q':
                t=lista_playlist[int(num)]
                write_playlist(text_name,t['owner']['id'],t['id'])
                i=i+1
            else:
                break
            
        #print(lista_playlist[int(num)]['id'])
        '''
        tracks = spobject.user_playlist('Spotify', playlist_id=lista_playlist[int(num)]['id'])['tracks']['items']
        print(json.dumps(tracks[0], indent=3))
        
        for tr in tracks:
            print(tr['track']['artists'][0]['name'] + " - " + tr['track']['name'])
        '''


        #print(lista_playlist)