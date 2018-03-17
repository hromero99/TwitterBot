import tweepy


@bot.message_handler(commands=['timeline']) #display timeline
def tweets_tl(api_object):
    tweets = api_object.home_timeline()
    for tweet in tweets:
        print(tweet.text)
        print("--------")