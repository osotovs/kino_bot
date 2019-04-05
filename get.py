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

def get_url_cinema(name_):              
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
    # proxies = {"http":"http://195.208.172.70:8080",,
    #     "https":"https://91.221.109.138:3128", "socks5": "socks5://138.197.157.32:1080"}
    try:
        result = requests.get(url)
        print(check_ip())
        result.raise_for_status()        
        return result.text        
    except(requests.RequestsException, ValueError):
        return False


def get_name_cinema(html):         
    soup = BeautifulSoup(html, "html.parser")
    name_cinema =  soup.findAll("a", itemprop="name")       
    list_cinemas = {}
    for name in name_cinema:         
        url_cinema = str(name).split("\"")
        nam = (f"К-р {name.text}")
        list_cinemas.update({nam:url_cinema[3]})                 
    dict_cinemas = list_cinemas               
    return(dict_cinemas)


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
    a_lists.append(["к списку городов","в начало"])
    return(a_lists)

def get_films(html):          
    soup = BeautifulSoup(html, "html.parser")    
    name_cinema = soup.findAll("div", class_="schedule-film__details")         
    return(name_cinema)


def check_ip():
	ip = requests.get('http://checkip.dyndns.org').content
	soup = BeautifulSoup(ip, 'html.parser')
	print(soup.find("body").text)





