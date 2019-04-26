from random import choice

from emoji import emojize
from telegram import ReplyKeyboardMarkup, KeyboardButton
from bs4 import BeautifulSoup
import requests


import settings




# city_list = {
#     "Томск": "https://www.afisha.ru/tomsk/cinema/cinema_list/",
#     "Москва": "https://www.afisha.ru/msk/cinema/cinema_list/",
#     "Петербург": "https://www.kinopoisk.ru/cinemas/tc/2/"
# }

# def get_url_cinema(name_):              
#     if name_ in city_list.keys():
#         return city_list.get(name_)


def get_user_emo(user_data):
    if"emo" in user_data:
        return user_data["emo"]
    else:
        user_data["emo"] = emojize(choice(settings.USER_EMOJI),use_aliases=True)
        return user_data["emo"]


def get_keyboard():
    my_keyboard = ReplyKeyboardMarkup([["поменять смайлик"],
        ["выбрать город"]],
        resize_keyboard=True)
    return(my_keyboard)

#"
# def get_html(url):
#     proxy = {"https":"https://94.242.59.135:655",
#         "https":"https://81.5.115.97:3128",
#         "https":"https://80.35.254.42:53281",
#         "https":"https://78.140.7.34:31222"
#         }        
#     try:
#         result = requests.get(url)
#         r = requests.get("https://ifconfig.me")#, proxies = proxy[2] )        
#         print(r.text)
#         result.raise_for_status()        
#         return result.text        
#     except(requests.RequestsException, ValueError):
#         return False


# def get_name_cinema(html):         
#     soup = BeautifulSoup(html, "html.parser")
#     name_cinema =  soup.findAll("a", itemprop="name")       
#     list_cinemas = {}
#     for name in name_cinema:         
#         url_cinema = str(name).split("\"")
#         nam = (f"К-р {name.text}")
#         list_cinemas.update({nam:url_cinema[3]})                 
#     dict_cinemas = list_cinemas               
#     return(dict_cinemas)


# def create_buttons_cinemas(dict_cinemas):
#     names = []
#     a_lists = []
#     for name in dict_cinemas:
#         names.append(name)   
#     while len(names) > 3:
#         three_cinema = names[:3]
#         a_lists.append(three_cinema)        
#         names = names[3:]
#     a_lists.append(names)   
#     a_lists.append(["к списку городов","в начало"])
#     return(a_lists)

# def get_films(html):          
#     soup = BeautifulSoup(html, "html.parser")    
#     name_cinema = soup.findAll("div", class_="schedule-film__details")         
#     return(name_cinema)


# def check_ip():
# 	ip = requests.get('http://checkip.dyndns.org').content
# 	soup = BeautifulSoup(ip, 'html.parser')
# 	print(soup.find("body").text)





