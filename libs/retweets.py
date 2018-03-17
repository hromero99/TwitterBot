import tweepy
import util from telebot

@bot.message_handler(commands=['rt'])
def retweet_tweets(message, api_object):
    tl = api_object.home_timeline()
    tweetsTBRT=util.extract_arguments(message.text)
    for n_tweets in tweetsTBRT:
        api_object.retweet(tl[n_tweets].id)

