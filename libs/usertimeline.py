import tweepy

def getUserTimeline(message, api, count=20):
    "Gets the timeline of an specified user"
    messageList = message.text.split()
    