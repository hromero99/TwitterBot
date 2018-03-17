import tweepy


def tweet(message, api, idToReply = None, mediaURI = None):
    "Function that sends tweet from your account"
    api.update_status(message, in_reply_to = idToReply, source = mediaURI)
    return 1

def getAPIObject(user_id):
    "Returns the api object for that user"
    with open("usuarios.json") as file: usuarios = json.load(file)
    listOfTokens = usuarios[user_id]
    auth = tweepy.OAuthHandler(str(listOfTokens[0]), str(listOfTokens[1]))
    auth.set_access_token(str(listOfTokens[2]), str(listOfTokens[3]))

    api = tweepy.API(auth)

    return api