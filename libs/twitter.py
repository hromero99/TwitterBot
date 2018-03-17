#-*-coding:utf-8 -*-
import tweepy
from telebot import util
from libs.bot_functions import *

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
    tl = api.home_timeline()
    imprimir(tl, bot, chat_id)
    tweetsTBRT=util.extract_arguments(message.text)
    for n_tweets in tweetsTBRT:
        api.retweet(tl[n_tweets].id)

def tweet_analytics(message):
    chat_id = message.chat.id
    api = getAPIObject(chat_id)
    tweets = api.user_timeline()
    imprimir(tweets, bot, chat_id)
    select = input("Ver las estadísticas del tweet nº ")
    bot.send_message(chat_id, "El número de RTs es %d" % (tweets[select].retweet_count))
    bot.send_message(chat_id, "El número de FAVs es %d" % (tweets[select].favorite_count))