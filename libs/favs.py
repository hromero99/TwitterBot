import tweepy
import util from telebot


@bot.message_handler(commands=['fav'])
def fav_tweets(message, api_object):
    tl = api_object.home_timeline()
    tweetsTBFAV=util.extract_arguments(message.text)
    for n_tweets in tweetsTBFAV:
        api_object.retweet(tl[n_tweets].id)
