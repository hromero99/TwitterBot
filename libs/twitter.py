#-*-coding:utf-8 -*-
import tweepy
from telebot import util
from libs.bot_functions import *

def tweet(text, api, idToReply = None, mediaURI = None):
    "Function for tweeting"
    #We have to split the text of the chat to tweet it

    if len(text.split()) > 1:
        messageList = text.split()[1:]
        messageText = str(messageList[0])
        #Append the rest of the list to the string so we can call the tweet function
        for i in messageList[1:]:
            messageText = messageText + " " + str(i)
        api.update_status(messageText, in_reply_to = idToReply, source = mediaURI)

        return "Tweet enviado"
    else:
        return "[!]Error, no se ha podido enviar tweets"

def fav_tweets(message):
    chat_id = message.chat.id
    api = getAPIObject(chat_id)
    tl = api.home_timeline()
    #imprimir(tl, bot, chat_id)
    tweetsTBFAV = util.extract_arguments(message.text)
    for n_tweets in tweetsTBFAV:
        api.favorite(tl[n_tweets].id)

def retweet_tweets(message):
    chat_id = message.chat.id
    api = getAPIObject(chat_id)
    #tl = api.home_timeline()
    #imprimir(tl, bot, chat_id)
    tweetsTBRT=util.extract_arguments(message.text)
    for n_tweets in tweetsTBRT:
        api.retweet(tl[n_tweets].id)

def tweet_analytics(message):
    chat_id = message.chat.id
    api = getAPIObject(chat_id)
    tweets = api.user_timeline()
    #imprimir(tweets, bot, chat_id)
    select = input("Ver las estadísticas del tweet nº ")
    bot.send_message(chat_id, "El número de RTs es %d" % (tweets[select].retweet_count))
    bot.send_message(chat_id, "El número de FAVs es %d" % (tweets[select].favorite_count))

def getTimeLineTweets(message, api, count=20):
    "Returns the tweets of the timeline of the user"
    return api.home_timeline()

def get_trending(api):

    trending = api.trends_place(766273)
    #Obtengo un diccionario de los hashtag
    hashtag = trending[0]['trends']
    utf_hashtag = []
    for tag in range(0,10):
        hashtag_string =  hashtag[tag]['name']

        utf_hashtag.append(hashtag_string)

    return  utf_hashtag