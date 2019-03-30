import logging
from random import choice

from get import get_keyboard, get_user_emo


def greet_user(bot, update,user_data):
    emo = get_user_emo(user_data)
    user_data["emo"] = emo
    text = f"привет {emo}"
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
