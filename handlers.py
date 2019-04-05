import logging
from random import choice
from telegram import replykeyboardremove, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler


from get import *
from bot import location_button, main

dict_cinemas = {}


def greet_user(bot, update, user_data):
    user_data["user_city"] = ("https://www.kinopoisk.ru/cinemas/tc/463/")
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
        "Отлично! Выбираем",
        reply_markup = ReplyKeyboardMarkup(reply_keyboard, 
        resize_keyboard=True))    
    # if reply_keyboard == location_button:        
    #     print(logging.info(text)    
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
    

def k_select_film(bot, update, user_data):
    user_text = update.message.text
    if user_text in dict_cinemas:               
        url = ("https://www.kinopoisk.ru" + (dict_cinemas.get(user_text)))                
        html = get_html(url)  
        films = get_films(html)        
        details = str(films)        
        soup = BeautifulSoup(details, "html.parser")        
        update.message.reply_text(soup.text)
        with open("afisha.html", "w", encoding = "utf-8") as film_detail:
            film_detail.write(str(soup))
        
        film = []
        a = soup.find_all("a", class_="schedule-film__title")
        spans = soup.find_all("div", class_ = "schedule-film__summary")			
        d = {}	
        for b in a:
            film += [(b.text)]

        detail = []
        for span in spans:
            detail += [(span.text)]	
        d.update(zip(film, detail))		
        for r  in d.keys():			
            name_film = (r)
            details_film = (d[r])
            update.message.reply_text(str(name_film), str(details_film))  
    elif user_text == "к списку городов" :
        return("select_city")    
    else:
        update.message.reply_text("чтотонетак")


def dontknow(bot, update, user_data):
    reply.message.reply_text("я не знаю")
   
