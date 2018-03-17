import tweepy
import json
from twitter import *

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
            return api

def checkApi(user_id):
    "Functions that check if an user can create the api"
    if user_id in usuarios.keys():
        listOfTokens = usuarios[str(user_id)]
        if len(listOfTokens) != 4:
            return False
        else:
            return True
