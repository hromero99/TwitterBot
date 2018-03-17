import telebot
import json
from libs.config import token
from libs.login_functions import *
from bot_functions import *

bot = telebot.TeleBot(token)

user_step={}

#Funcion para obtener donde se encuentra el usuario

def get_user_sept(chat_id):
    if chat_id in user_step:
        return user_step[chat_id]
    else:
        add_user(chat_id)
        user_step[chat_id] = 0
        return 0

#Comando de bienvenida

@bot.message_handler(commands=["start"])
def bot_starting(message):
    chat_id = message.chat.id
    if is_user(chat_id):
        bot.send_message(chat_id,"Bienvenido...")
    else:
        bot.send_message(chat_id, add_user(chat_id))
        user_step[chat_id] = 0


#Funcion para registrar nuevos usuarops o sobreescribir la informacion del usuario existente
@bot.message_handler(commands=["register"])
def register_function(message):
    chat_id = message.chat.id
    #TODO: Add some restrictions to the register
    if ( len (usuarios[str(chat_id)]) == 4):
        bot.send_message(chat_id,"Ya has introducido los datos, tienes que hacer un delete")

    bot.send_message(chat_id,"Procede a introducir la informacion")
    bot.send_message(chat_id,"Introduce el consumer key")
    user_step[chat_id] = 1

@bot.message_handler(func=lambda message: get_user_sept(message.chat.id) == 1)
def consumer_key(message):
    chat_id  = message.chat.id
    key = message.text
    if (len(str(key)) != 25):
        bot.send_message(chat_id, "La longitud de la clave introducida no es correcta")
    else:
        write_db(chat_id,key)
        bot.send_message(chat_id, "Introduce el Consumer Secret Key")
        user_step[chat_id] = 2


@bot.message_handler(func=lambda message: get_user_sept(message.chat.id) == 2)
def consumer_secret_key(message):
    chat_id = message.chat.id
    key = message.text
    if len(str(key)) != 50:
        bot.send_message(chat_id, "La longitud de la clave introducida no es correcta")
    else:
        # The key has the stimated length so we can continue
        write_db(chat_id,key)
        bot.message_handler(chat_id,"Introduce el Access_token_key")
        # Add one more to the users step
        user_step[chat_id] += 1


@bot.message_handler(func=lambda message: get_user_sept(message.chat.id) == 3)
def access_token_key(message):
    chat_id = message.chat.id
    key = message.text

    if len(key) != 50:
        bot.send_message(chat_id, "La longitud de la clave introducida no es correcta")
    else:
        # The key has the stimated length so we can continue
        write_db(chat_id,key)
        # Add one more to the users step
        user_step[chat_id] += 1
        bot.message_handler(chat_id, "Introduce al access token secret/")


@bot.message_handler(func=lambda message: get_user_sept(message.chat.id) == 4)
def access_token_secret_key(message):
    chat_id = message.chat.id
    key = message.text
    if len(key) != 45:
        bot.send_message(chat_id, "La longitud de la clave introducida no es correcta")
    else:
        # The key has the stimated length so we can continue
        write_db(chat_id,key)
        # Add one more to the users step

    user_step[chat_id] = -1

@bot.message_handler(commands=["tweet"])
def twettMessage(message):
    "Tweets the message appended in this command"
    messageText = message.text.split()[1:]
    api = getAPIObject(message.chat.id)
    tweet(str(messageText), api)
    bot.send_message(message.chat.id, "Tweet enviado!")

@bot.message_handler(commands=['fav'])
def fav_tweets(message, api_object):
    tl = api_object.home_timeline()
    tweetsTBFAV=util.extract_arguments(message.text)
    for n_tweets in tweetsTBFAV:
        api_object.retweet(tl[n_tweets].id)

@bot.message_handler(commands=['rt'])
def retweet_tweets(message, api_object):
    tl = api_object.home_timeline()
    tweetsTBRT=util.extract_arguments(message.text)
    for n_tweets in tweetsTBRT:
        api_object.retweet(tl[n_tweets].id)

@bot.message_handler(commands=['timeline']) #display timeline
def tweets_tl(api_object):
    tweets = api_object.home_timeline()
    for tweet in tweets:
        print(tweet.text)
        print("--------")

@bot.message_handler(commands=["del"])
def del(message):
    chat_id = message.cha.id
    bot.send_message(chat_id,del_user(chat_id))

bot.polling(True)
