import tweepy
import json


#Cargamos la base de datos de usuarios
with open("usuarios.json") as file: usuarios = json.load(file)


def is_user(chat_id):
    if   ( usuarios.get(str(chat_id)) ) == None:
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
        print "You should delete your user first"
    with open("usuarios.json","w") as file: json.dump(usuarios,file,indent=2)


