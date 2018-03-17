import tweepy
from bot_functions import *



def get_trending(api):

    trending = api.trends_place()

    hashtag = trending[0]['trends']
    utf_hashtag = []
    for tag in range(0,len(hashtag)):
        hashtag_string = hashtag[tag]['name']
        if hashtag_string[0] == "#":

            utf_hashtag.append(hashtag_string)

    return  utf_hashtag