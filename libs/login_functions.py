import tweepy
import json


#Cargamos la base de datos de usuarios
with open("usuarios.json") as file: usuarios = json.load(file)


def is_user(chat_id):
    if usuarios.get(str(chat_id)) != None:
        return True
    else:
        return False

def save_user():

    with open("usuarios.json","w") as file: json.dump(usuarios,file,indent=2)

def add_user(chat_id):
    if (is_user(chat_id)):
        return "Ya eres un usuario"
    else:
        usuarios[str(chat_id)] = {}
        save_user()
        return "Usuario agregado correctamente"


def write_db(chat_id,values):
    #0--> consumer key
    #1 --> consumer secret
    #2 --> access token
    #3 > access token secret
    usuarios[chat_id].append(values)

    with open("usuarios.json","w") as file: json.dump(usuarios,file,indent=2)


