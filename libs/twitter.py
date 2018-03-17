import tweepy
from telebot import util

def fav_tweets(message, api_object):
    tl = api_object.home_timeline()
    #funcion imprimir
    tweetsTBFAV = util.extract_arguments(message.text)
    for n_tweets in tweetsTBFAV:
        api_object.retweet(tl[n_tweets].id)

def retweet_tweets(message, api_object):
    tl = api_object.home_timeline()
    '''funcion imprimir'''
    tweetsTBRT=util.extract_arguments(message.text)
    for n_tweets in tweetsTBRT:
        api_object.retweet(tl[n_tweets].id)

def tweet_analytics(message, api_object, bot):
    tweets = api_object.user_timeline()
    '''funcion imprimir'''
    select = input("Ver las estadísticas del tweet nº ")
    bot.send_message(message.chat.id, "El número de RTs es %d" % (tweets[select].retweet_count))
    bot.send_message(message.chat.id, "El número de FAVs es %d" % (tweets[select].favorite_count))