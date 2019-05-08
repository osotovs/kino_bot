import logging
from random import choice
from telegram import replykeyboardremove, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler

from get import *
from bot import location_button, main
from citie import *

dict_cinemas = {}

def greet_user(bot, update, user_data):
    bot.send_sticker(chat_id = update.message.chat_id, sticker = open("images/sticker_hi.webp","rb"))       
    emo = get_user_emo(user_data)
    user_data["emo"] = emo
    text = f"""Привет, {update.message.chat.first_name} {emo}.
Я Бот, который поможет тебе
узнать какие фильмы показывают сейчас в кинотеатрах.
Выбери, пожалуйста город, в котором ты находишься и приступим{emo}.
"""
    logging.info   
    update.message.reply_text(text, reply_markup = get_keyboard())
    

def talk_to_me(bot, update,user_data):
    try:
        show_waiting(bot, update, user_data)
    except:
        try:
            get_user_emo(user_data)
            text = update.message.text        
            update.message.reply_text("{}, ты написал {} {}".format(update.message.chat.first_name, 
                text, user_data["emo"]), reply_markup = get_keyboard())
            logging.info(text)
        except:
            update.message.reply_text("что то пошло не так")


def change_ava(bot, update, user_data):
    if "emo" in user_data:
        del user_data["emo"]
    emo = get_user_emo(user_data)
    update.message.reply_text((f"готово!{emo}"), reply_markup = get_keyboard())


def k_select_city(bot, update, user_data):
    reply_keyboard = [["Томск","Москва","Петербург"],
        [location_button]]
    update.message.reply_text(
        "Если Вашего города нет в списке, напишите мне его" + user_data["emo"],
        reply_markup = ReplyKeyboardMarkup(reply_keyboard, 
        resize_keyboard=True))       
    return ("select_cinema") 


def k_select_cinema(bot, update, user_data):
    if update.message.text in city_list:
        user_city = update.message.text
        user_data["user_city"] = user_city    
        html = get_url_cinema(user_city)
        url = get_html(html)
        dict_cinema = get_name_cinema(url)
        global dict_cinemas
        dict_cinemas = dict_cinema
        list_cinemas = create_buttons_cinemas(dict_cinema)
        reply_keyboard = list_cinemas
        update.message.reply_text("Выбираем кинотеатр",
            reply_markup = ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True))           
        return("select_film")
    else:
        update.message.reply_text("""у меня пока нет данных по этому городу
            выбери из списка""")


def stop_conv_hand(bot, update, user_data):    
    return ConversationHandler.END


def dontknow(bot, update, user_data):
    reply.message.reply_text("я не знаю")
   
