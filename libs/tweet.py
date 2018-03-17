import tweepy

def tweet(text, api, idToReply = None, mediaURI = None):
    "Function for tweeting"
    #We have to split the text of the chat to tweet it
    if len(text) > 1: 
        messageList = text.split()[1:]
        messageText = str(messageList[0])
        #Append the rest of the list to the string so we can call the tweet function
        for i in messageList[1:]:
            messageText = messageText + " " + str(i)
        api.update_status(messageText, in_reply_to = idToReply, source = mediaURI)
