import telebot
from telebot import *
import json
from libs.trendings import *
from libs.config import token
from libs.login_functions import *
from libs.bot_functions import *
from libs.tweet import *
from libs.twitter import *


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

def send_to_register(chat_id):
    bot.send_message(chat_id,"Error, tienes que registrar los datos")

keyboard = types.InlineKeyboardMarkup()
keyboard.add(types.InlineKeyboardButton('RT', callback_data='rt'),
             types.InlineKeyboardButton('Fav', callback_data='fav'))


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
    if is_user(chat_id):
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
        bot.send_message(chat_id,"Introduce el Access_token_key")
        # Add one more to the users step
        user_step[chat_id] = 3


@bot.message_handler(func=lambda message: get_user_sept(message.chat.id) == 3)
def access_token_key(message):
    chat_id = message.chat.id
    key = message.text

    if len(key) != 50:
        bot.send_message(chat_id, "La longitud de la clave introducida no es correcta")
    else:
        # The key has the stimated length so we can continue
        write_db(chat_id,key)
        bot.send_message(chat_id, "Introduce al access token secret/")
        # Add one more to the users step
        user_step[chat_id] = 4


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
        bot.send_message(chat_id,"Datos registrados correctamente")
    user_step[chat_id] = -1


@bot.message_handler(commands=['fav'])
def bot_fav(message):
    fav_tweets(message)

@bot.message_handler(commands=['rt'])
def bot_rt(message):
    retweet_tweets(message)

@bot.message_handler(commands=['timeline'])
def bot_displayinfo(message):
    if is_user(message.chat.id):
        api =getAPIObject(message.chat.id)

        timeLine = getTimeLineTweets(message, api)
        #Now we have to print the tweets in the chat
        for tweet in timeLine:
            bot.send_message(message.chat.id, str(tweet.text), reply_markup=keyboard)
    else:
        send_to_register(message.chat.id)

@bot.message_handler(commands=["del"])
def delete(message):
    chat_id = message.chat.id
    bot.send_message(chat_id,del_user(chat_id))

#Comenzamos a usar la API

@bot.message_handler(commands=["tweet"])
def twettMessage(message):
    "Tweets the message appended in this command"
    if is_user(message.chat.id):
        api =getAPIObject(message.chat.id)

        bot.send_message(message.chat.id,tweet(message.text, api))
    else:
        send_to_register(message.chat.id)

@bot.message_handler(commands=["trends"])
def send_trends(message):
    api = getAPIObject(message.chat.id)
    trendings = get_trending(api)
    for x in trendings:
        bot.send_message(message.chat.id, x)


@bot.inline_handler(func=lambda query: True)
def inline_trends(message):
    user_id = message.from_user.id
    if  not is_user(user_id):
        return
    api = getAPIObject(user_id)
    trendings = get_trending(api)
    i = 0
    lista = []
    for trend in trendings:
        lista.append(
            types.InlineQueryResultArticle(
                i,
                trend,
                types.InputTextMessageContent(trend,parse_mode="Markdown"),
                description=None
            )
        )
        i = i+1
    bot.answer_inline_query(message.id,lista,cache_time=100)

@bot.callback_query_handler(func=lambda call: call.data == "rt")
def callback_Rt:
    "function for the rt of a tweet"
    print "RT"

@bot.callback_query_handler(func=lambda call: call.data == "fav")
def callback_Rt:
    "function fot the fav of a tweet"
    print "Fav"

bot.polling(True)
