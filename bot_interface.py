# -*- coding: utf-8 -*-
import telebot
from telebot import *
import json
from libs.config import token
from libs.bot_functions import *
from libs.twitter import *
from libs.keyboards import *

bot = telebot.TeleBot(token)

listOfTweets = {}

# Teclados




def send_to_register(chat_id):
    "Funcion para indicar al usuario que tiene que registrarse"
    bot.send_message(chat_id, "Error, tienes que registrar los datos")


# Comando de ayuda de usuario
@bot.message_handler(commands=["help"])
def say_help(message):
    "Funcion para mostrar el mensaje de ayuda"
    bot.send_message(message.chat.id,
                     "Bienvenido a TwitterControleBot para poder usar correctamente tienes que obtener tus credenciales dirigete a \t https://dev.twitter.com/apps/new \t y posteriormente puedes registrarte con /register"
                     )


# Comando de bienvenida

@bot.message_handler(commands=["start"])
def bot_starting(message):
    "Funcion de comienzo del bot"
    chat_id = message.chat.id
    if is_user(chat_id):
        bot.send_message(chat_id, "Bienvenido de nuevo")
    else:
        bot.send_message(chat_id, add_user(chat_id))
        say_help(message)


# Funcion para registrar nuevos usuarops o sobreescribir la informacion del usuario existente

@bot.message_handler(commands=["register"])
def register_function(message):
    "Funcion para registrar los datos del usuario"

    chat_id = message.chat.id

    if is_user(chat_id):
        bot.send_message(chat_id, "Ya has introducido los datos, tienes que hacer un delete")
    else:
        bot.send_message(chat_id, "Procede a introducir la informacion")
        bot.send_message(message.chat.id, "Introduce el Consumer Key")
        bot.register_next_step_handler(message, regConsumerKey)


def regConsumerKey(message):
    if (len(str(message.text)) != 25):
        bot.send_message(message.chat.id, "La longitud de la clave introducida no es correcta")
    else:
        write_db(message.chat.id, message.text)
        bot.send_message(message.chat.id, "Introduce el Consumer Secret")
        bot.register_next_step_handler(message, regConsumerSecret)


def regConsumerSecret(message):
    chat_id = message.chat.id
    key = message.text
    if len(str(key)) != 50:
        bot.send_message(chat_id, "La longitud de la clave introducida no es correcta")
    else:
        # The key has the stimated length so we can continue
        write_db(chat_id, key)
        bot.send_message(chat_id, "Introduce el Access Token")
        bot.register_next_step_handler(message, regAccessToken)


def regAccessToken(message):
    key = message.text
    chat_id = message.chat.id
    if len(key) != 50:
        bot.send_message(chat_id, "La longitud de la clave introducida no es correcta")
    else:
        write_db(chat_id, key)
        # Add one more to the users step
        bot.send_message(chat_id, "Introduce el Access Token Key")
        bot.register_next_step_handler(message, regAccessTokenKey)


def regAccessTokenKey(message):
    chat_id = message.chat.id
    key = message.text
    if len(key) != 45:
        bot.send_message(chat_id, "La longitud de la clave introducida no es correcta")
    else:
        # The key has the stimated length so we can continue
        write_db(chat_id, key)

        bot.send_message(chat_id, "Datos registrados correctamente")



@bot.message_handler(commands=["del"])
def delete(message):
    "Funcion para eliminar los usuarios"
    chat_id = message.chat.id
    if (is_user(chat_id)):

        # del_user devulve directamente el mensaje
        bot.send_message(chat_id, del_user(chat_id))
    else:
        bot.send_message(chat_id, "No te has registrado aún")


# Comenzamos a usar la API

@bot.message_handler(commands=["tweet"])
def twettMessage(message):
    "Tweets the message appended in this command"
    if is_user(message.chat.id):
        api = getAPIObject(message.chat.id)

        bot.send_message(message.chat.id, tweet(message.text, api))
    else:
        send_to_register(message.chat.id)


@bot.message_handler(commands=["trends"])
def send_trends(message):
    "Funcion para consultar los Trending Topics"

    api = getAPIObject(message.chat.id)
    trendings = get_trending(api)
    for trending in trendings:
        bot.send_message(message.chat.id, trending)


@bot.inline_handler(func=lambda query: True)
def inline_trends(message):
    "Funcion para manejar las consultas Inline de los Trendings"
    user_id = message.from_user.id
    if not is_user(user_id):
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
                types.InputTextMessageContent(trend, parse_mode="Markdown"),
                description=None
            )
        )
        i = i + 1
    bot.answer_inline_query(message.id, lista, cache_time=100)


@bot.callback_query_handler(func=lambda call: call.data == "rt")
def callback_Rt(call):
    "function for the rt of a tweet"
    # Rt the tweet
    api = getAPIObject(call.message.chat.id)
    api.retweet(int(listOfTweets[call.message.message_id][0]))
    bot.send_message(call.message.chat.id, "RT guardado!")


@bot.callback_query_handler(func=lambda call: call.data == "fav")
def callback_fav(call):
    "function for giving a fav to a tweet"
    api = getAPIObject(call.message.chat.id)
    api.create_favorite(int(listOfTweets[call.message.message_id][0]))
    bot.send_message(call.message.chat.id, "Favorito guardado!")




@bot.message_handler(commands=['fav'])
def bot_fav(message):
    fav_tweets(message)


@bot.message_handler(commands=['rt'])
def bot_rt(message):
    retweet_tweets(message)


@bot.message_handler(commands=['timeline'])
def showTimeLine(message):
    "Function to display the user timeline"
    if is_user(message.chat.id):
        api = getAPIObject(message.chat.id)

        timeLine = getTimeLineTweets(message, api)
        # Now we have to print the tweets in the chat
        for tweet in timeLine:
            textoAEnviar = u'@'.join((tweet.user.screen_name, "\n", tweet.text)).encode("utf-8").strip()
            msg = bot.send_message(message.chat.id, textoAEnviar, reply_markup=keyboard)
            listOfTweets[msg.message_id] = [int(tweet.id)]
    else:
        send_to_register(message.chat.id)
bot.polling(True)
