import logging
from random import choice
from telegram import replykeyboardremove, ReplyKeyboardMarkup

from get import get_keyboard, get_user_emo


def greet_user(bot, update,user_data):
    emo = get_user_emo(user_data)
    user_data["emo"] = emo
    text = f"""Привет, {update.message.chat.first_name} {emo}.
    Я Бот, который легко поможет тебе
    узнать какие фильмы показывают сейчас в кинотеатрах.
    Выбери, пожалуйста город, в котором ты находишься иприступим{emo}.
    По умолчанию это Томск{emo}
    """
    logging.info   
    update.message.reply_text(text, reply_markup = get_keyboard())


def talk_to_me(bot, update,user_data):
    get_user_emo(user_data)
    text = update.message.text
    print(text)
    update.message.reply_text("{}, ты написал {} {}".format(update.message.chat.first_name, 
        text, user_data["emo"]), reply_markup = get_keyboard())
    logging.info(text)


def change_ava(bot, update, user_data):
    if "emo" in user_data:
        del user_data["emo"]
    emo = get_user_emo(user_data)
    update.message.reply_text((f"готово!{emo}"), reply_markup = get_keyboard())


def k_select_city(bot, update, user_data):
    reply_keyboard = [["Томск","Москва","Питербург"]]
    update.message.reply_text(
        "Отлично! Выбираем",
        reply_markup = ReplyKeyboardMarkup(reply_keyboard, 
        one_time_keyboard = True, resize_keyboard=True))
    return("select_cinema")

def k_select_cinema(bot, update, user_data):
    user_city = update.message.text
    user_data["user_city"] = user_city
    update.message.reply_text("Выбираем кинотеатр")