# -- coding: utf-8 --
import city

from bs4 import BeautifulSoup
import requests
import logging
import re
import time

from fake_useragent import UserAgent
from telegram import replykeyboardremove, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler

import socks
import socket

socks.set_default_proxy(socks.SOCKS5, "localhost", 9150)
socket.socket = socks.socksocket

logging.basicConfig(format = "%(name)s - %(levelname)s - %(message)s",
                    level = logging.INFO,
                    filename = "bot.log")

ua = UserAgent()
dict_kinoteatr= {}

def get_times(link):		
	r = requests.get(link).text	
	print(r)	
	soup = BeautifulSoup(r, "html.parser")			
	lfs = soup.find_all("div", class_ =("schedule-item"))
	list_films = []		
	result = ""
	addres = soup.find("div", class_=("cinema-header__address"))
	result += ("\n\n" + addres.text + "\n")
	for lf in lfs:		
		lts = lf.find_all("div", class_ =("schedule-film__details"))		
		for lt in lts:			
			dts = lt.find_all("a", class_ = ("link", "schedule-film__title"))				
			dict_titles = {}
			titles = []
			for tit in dts:				
				t=tit.text
				result += ("\n  " + t + "\n")				
				l_gs = lt.find_all("div", class_ = ("schedule-film__summary"))
				d_fs = lf.find_all("span", class_ = ("schedule-item__formats-format"))
				p_ts = lf.find_all("span", class_ = ("schedule-item__session-button-wrapper"))
				list_general = []
				dict_formats = {}
				for lg in l_gs:					
					lg = lg.text
					result += (lg + "\n")					
					list_general.append(lg)
				for df in d_fs:					
					d= df.text
					result += ("\n  "+d + ":\n")					
					time_price = []
					for pt in p_ts:						
						p = pt.text						
						times = pt.find_all("span", class_ = ("schedule-item__session-button"))
						price = pt.find_all("span", class_ = ("schedule-item__price"))
						for time in times:
							t= (time.text)
						for pric in price:
							p = (pric.text)							
						pr_ti =(t + "- " + p)
						result += (pr_ti + "\n")												
						t = for_in(times)
						p = for_in(price)
						t.extend(p)								
						time_price.append(t)								
				dict_formats[d] = time_price
			list_general.append(dict_formats)					
			titles.append(t)				
		list_films.append(list_general)	
	if len(result) > 0:
		return(result)
	else:
		return("опять забанили")

		
def get_kinoteatr(text):		
	url = city.CITY_LIST.get(text)	
	print("1", url)
	time.sleep(1)
	r = requests.get(url).text	
	soup = BeautifulSoup(r, "html.parser")		
	name_kinoteatr = soup.find_all("a", itemprop= "name")
	print("2", name_kinoteatr)
	links = []	
	cin = []	
	d = {}
	for once in name_kinoteatr:
		d[once.text] = once.get("href")		
	global dict_kinoteatr
	dict_kinoteatr = d
	print (d)
	return(d)


def get_list_kinoteatr(bot, update, user_data):	
	user_tex = (update.message.text).capitalize()
	
	dict_kinoteatr = get_kinoteatr(user_tex)
	if (dict_kinoteatr) == {}:
		update.message.reply_text("К сожалению я пока не знаю об этом городе")
	else:
		names_kinoteatr = list(dict_kinoteatr.keys())
		reply_keyboard = create_buttons(names_kinoteatr)
		update.message.reply_text(
			"Отлично! Выбираем, куда пойдем",
			reply_markup = ReplyKeyboardMarkup(reply_keyboard, 
			resize_keyboard=True)) 	
		return("select_film")


def kino_details(bot, update, user_data):
	user_text = update.message.text	
	if (user_text) == "к списку городов":
		return "select_city"
	if user_text in dict_kinoteatr:
		a = dict_kinoteatr.get(user_text)		
		d = get_times("https://www.kinopoisk.ru" + str(a))
		print(d)	
		get_map("https://www.kinopoisk.ru" + str(a))
		bot.send_photo(chat_id = update.message.chat_id, photo = open("images/foto.jpg","rb"))
		update.message.reply_text(d)		
	else:				
		update.message.reply_text("что-то не так, давай ка сначала",
			reply_markup = ReplyKeyboardMarkup([["start"]],resize_keyboard=True))
		return (ConversationHandler.END)


def create_buttons(list_):
	list_buttons = []
	while len(list_) > 2:
		para_buttons = list_[:2]
		list_buttons.append(para_buttons)        
		list_ = list_[2:]
	list_buttons.append(list_)   
	list_buttons.append(["к списку городов"])
	return(list_buttons)

			
def for_in(lists):
	d = []
	for list_ in lists:
		d += [(list_.text)]
	return(d)	


def get_map(url):
	proxy = {"https":"https://94.242.59.135:655",
      
        }        
	# url = "https://www.kinopoisk.ru/afisha/city/450/cinema/263968/"
	time.sleep(1)
	resp = requests.get(url).text# proxies = proxy).text
	soup = BeautifulSoup(resp, "html.parser")	
	s = soup.find("div", class_=("cinema-header__map"))		
	img = s.find("img", class_ = ("image-partial-component","image-partial-component_loaded"))["src"]	
	f = open("images/foto.jpg", "wb")
	r = requests.get(img)
	f.write(r.content)
	f.close()

def check_ip():
	url = 'http://icanhazip.com/'
	out = requests.get(url).text
	# out = (out.replace('\n',''))
	print (out)

def g():
	for i in range(10):
		check_ip()
		time.sleep(5)

if __name__ == "__main__":
	# get_map()
	g()
	
	
