from random import choice

from emoji import emojize
from telegram import ReplyKeyboardMarkup, KeyboardButton
from bs4 import BeautifulSoup
import requests
import datetime

import settings

td = datetime.datetime.now()
date = td.strftime("%Y-%m-%d")

city_list = {
    "Томск": "https://www.kinopoisk.ru/cinemas/tc/463/",
    "Москва": "https://www.kinopoisk.ru/cinemas/tc/1/",
    "Петербург": "https://www.kinopoisk.ru/cinemas/tc/2/"
}

def get_url_cinema(name_):              #находим url кинотеатра
    if name_ in city_list.keys():
        return city_list.get(name_)


def get_user_emo(user_data):
    if"emo" in user_data:
        return user_data["emo"]
    else:
        user_data["emo"] = emojize(choice(settings.USER_EMOJI),use_aliases=True)
        return user_data["emo"]


def get_keyboard():
    my_keyboard = ReplyKeyboardMarkup([["start", "ава"],
        ["выбрать город"],["выбрать кинотеатр"]],
        resize_keyboard=True)
    return(my_keyboard)


def get_html(url):
    try:
        result = requests.get(url)
        result.raise_for_status()        
        return result.text        
    except(requests.RequestsException, ValueError):
        return False


def get_name_cinema(html):          #возващаем словарь к-р:url
    soup = BeautifulSoup(html, "html.parser")
    name_cinema =  soup.findAll("a", itemprop="name")       
    list_cinemas = {}
    for name in name_cinema: 
        url_cinema = str(name).split("\"")
        nam = (f"К-р {name.text}")
        list_cinemas.update({nam:url_cinema[3]})           
    dict_cinemas = list_cinemas      
    return(dict_cinemas)

# # html = "https://www.kinopoisk.ru/cinemas/tc/463/"
# dict_cinemas = {} 
# url_cinema = ""

# # my_keyboard = get_html("https://www.kinopoisk.ru/cinemas/tc/463/")

# # contact_button = KeyboardButton("РїСЂРёСЃР»Р°С‚СЊ РєРѕРЅС‚Р°РєС‚С‹", request_contact = True)
# # location_button = KeyboardButton("РїСЂРёСЃР»Р°С‚СЊ РіРµРѕРґР°РЅРЅС‹Рµ", request_location = True)
 

# # def get_afisha(name_ci, dict_cinemas):
# #     print(dict_cinemas)
# #     if name_ci in dict_cinemas:    
# #         value = dict_cinemas[name_ci]
# #         url_afisha = ((html[0:-1]) + value)
# #         print(value)
# #     global url_cinema
# #     url_cinema = (f"https://www.kinopoisk.ru{value}")
# #     print(url_cinema)

def create_buttons_cinemas(dict_cinemas):
    names = []
    a_lists = []
    for name in dict_cinemas:
        names.append(name)   
    while len(names) > 3:
        three_cinema = names[:3]
        a_lists.append(three_cinema)        
        names = names[3:]
    a_lists.append(names)           
    return(a_lists)



def but_cin(list_buttons):  
    dict_cinemas = list_buttons         
    buttons = ([])
    a_lists =([])
    for para in list_buttons:        
        buttons.append(para)
    print(buttons[1])
    # get_afisha(buttons[1],dict_cinemas)    
    while len(buttons) > 3:
        a_list = buttons[:3]
        a_lists.append(a_list)        
        buttons = buttons[3:]        
    a_lists.append(buttons) 
    list_buttons =add_default_buttons(a_lists)        
    return(list_buttons)

# def add_default_buttons(lsits):
#     lsits.append(["РїСЂРёСЃР»Р°С‚СЊ Р»РёСЃР°", "СЃРјРµРЅРёС‚СЊ Р°РІР°С‚Р°СЂ"]
#                 # [contact_button, location_button]
#                 )    
#     print(dict_cinemas)
#     return(lsits)

# # def get_list_films_of_cinema(bot,update,user_data):
# #     user_text = update.message.text   
# #     get_afisha(user_text, dict_cinemas)
# #     print(url_cinema)
# #     url = (f"{url_cinema}day_view/{date}/")
# #     print(url)
# #     html = get_html(url)
# #     soup = BeautifulSoup(html, "html.parser")
# #     name_film = soup.findAll(itemprop= "name")
# #     name = gen_list(name_film)
# #     print( name_film)

# #     def gen_list(items_):
# #         for item_ in items_:
# #             yield item_

# def start():
#     html = get_html("https://www.kinopoisk.ru/cinemas/tc/1/")
#     print(html)
#     if html:
#         get_name_cinema(html)
    
#     # update.message.reply_text(name_film.text)
#     # print(str(name_film.text))

# # result_buttons = get_name_cinema(get_html(html)) 

# # get_city(get_html(html))

# # get_name_cinema(get_html(html))

# # result = requests.get('http://api.kinopoisk.cf/getFilm?filmID=843859')

# # print (result.text)