import tweepy
import json
from twitter import *
import time

with open("./usuarios.json") as file: usuarios = json.load(file)

def getAPIObject(user_id):
    "Returns the api object for that user"
    listOfTokens = usuarios.get(str(user_id))
    if listOfTokens:
        if len(listOfTokens) == 4:
            auth = tweepy.OAuthHandler(str(listOfTokens[0]), str(listOfTokens[1]))
            auth.set_access_token(str(listOfTokens[2]), str(listOfTokens[3]))
            api = tweepy.API(auth)
            #The user cannot create the api cause it's not registered
            time.sleep(1)
            return api

def checkApi(user_id):
    "Functions that check if an user can create the api"
    if user_id in usuarios:
        listOfTokens = usuarios[str(user_id)]
        if len(listOfTokens) != 4:
            return False
        else:
            return True

'''Login Functions'''


def is_user(chat_id):
    if   ( usuarios.get(str(chat_id)) ) == None or  (len(usuarios.get(str(chat_id))) != 4 ):
        return False
    else:
        return True



def save_user():

    with open("usuarios.json","w") as file: json.dump(usuarios,file,indent=2)

def add_user(chat_id):
    if (is_user(chat_id)):
        return "Ya eres un usuario"
    else:
        usuarios[str(chat_id)] = []
        save_user()
        return "Usuario agregado correctamente"


def write_db(chat_id,values):
    #.append(str(values))
    datos  =  usuarios[str(chat_id)]

    if (len(datos) != 4):
        datos.append(str(values))
    else:
        print("You should delete your user first")
    with open("usuarios.json","w") as file: json.dump(usuarios,file,indent=2)


def del_user(chat_id):
    try:
        usuarios[str(chat_id)] = []
        save_user()
        return  "Usuario elminado correctamente"
    except:
        return "Error al eliminar el usuario"
