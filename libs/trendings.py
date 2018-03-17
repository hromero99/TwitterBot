import tweepy
from bot_functions import *

def get_trending(api):

    trending = api.trends_place(766273)
    #Obtengo un diccionario de los hashtag
    hashtag = trending[0]['trends']
    utf_hashtag = []
    for tag in range(0,10):
        hashtag_string =  hashtag[tag]['name']

        utf_hashtag.append(hashtag_string)

    return  utf_hashtag