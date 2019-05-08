# -- coding: utf-8 --
import city

from bs4 import BeautifulSoup
import requests
import logging
import re
import time
import datetime

from fake_useragent import UserAgent
from telegram import replykeyboardremove, ReplyKeyboardMarkup, ParseMode,\
	InlineKeyboardButton, InlineKeyboardMarkup 
from telegram.ext import Updater, CommandHandler, MessageHandler, \
	Filters, RegexHandler, ConversationHandler

import socks
import socket

td = datetime.datetime.now()
date = td.strftime("%Y-%m-%d")
nd = td + datetime.timedelta(days = 1)
next_day = nd.strftime("%Y-%m-%d")

socks.set_default_proxy(socks.SOCKS5, "localhost", 9150)
socket.socket = socks.socksocket

logging.basicConfig(format = "%(name)s - %(levelname)s - %(message)s",
                    level = logging.INFO,
                    filename = "bot.log")

ua = UserAgent()
dict_kinoteatr= {}
url_times = ""
day = ""
dict_waiting= {}

def get_times(link):		
	r = requests.get(link).text	
	print(r)	
	day = den(link)
	soup = BeautifulSoup(r, "html.parser")			
	lfs = soup.find_all("div", class_ =("schedule-item"))
	list_films = []		
	result = ""
	addres = soup.find("div", class_=("cinema-header__address"))
	result += ("\n\n" + addres.text + "\n<b>Расписание на </b>"+day + "\n")
	for lf in lfs:		
		lts = lf.find_all("div", class_ =("schedule-film__details"))		
		for lt in lts:			
			dts = lt.find_all("a", class_ = ("link", "schedule-film__title"))				
			dict_titles = {}
			titles = []
			for tit in dts:				
				t=tit.text
				result += ("\n  <b>" + t + "</b>\n")				
				l_gs = lt.find_all("div", class_ = ("schedule-film__summary"))
				d_fs = lf.find_all("span", class_ = ("schedule-item__formats-format"))
				p_ts = lf.find_all("span", class_ = ("schedule-item__session-button-wrapper"))
				list_general = []
				dict_formats = {}
				for lg in l_gs:					
					lg = lg.text
					result += ("<i>" + lg + "</i>\n")					
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
	if len(result) > 0:
		return(result)
	else:
		return("опять забанили")


def den(text):
	result = text[-11:-1]
	global day
	day = result
	return result

		
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
	if user_tex in city.CITY_LIST.keys():		
		dict_kinoteatr = get_kinoteatr(user_tex)
		names_kinoteatr = list(dict_kinoteatr.keys())
		reply_keyboard = create_buttons(names_kinoteatr)
		update.message.reply_text(
			"Отлично! Выбираем, куда пойдем" + user_data["emo"],
			reply_markup = ReplyKeyboardMarkup(reply_keyboard, 
			resize_keyboard=True)) 	
		return("select_film")
	else:
		update.message.reply_text("К сожалению я пока не знаю об этом городе")	
		bot.send_sticker(chat_id = update.message.chat_id, sticker = open("images/sticker_dont_know.webp","rb"))
	

def kino_details(bot, update, user_data):
	user_text = update.message.text	
	if (user_text) == "к списку городов":
		return "select_city"
	if user_text in dict_kinoteatr:
		a = dict_kinoteatr.get(user_text)
		global url_times
		url_times = "https://www.kinopoisk.ru" + str(a)		
		d = get_times(url_times + "day_view/" + date + "/")
		print(d)	
		get_map("https://www.kinopoisk.ru" + str(a))
		bot.send_photo(chat_id = update.message.chat_id, photo = open("images/foto.jpg","rb"))
		update.message.reply_text(d, parse_mode = ParseMode.HTML,reply_markup = show_inline(bot,update))		
	else:				
		update.message.reply_text("что-то не так, выберите из списка или к началу",
			reply_markup = ReplyKeyboardMarkup([["start"]],resize_keyboard=True))
		return (ConversationHandler.END)


def show_inline(bot, update):
	inlinekbd = [[InlineKeyboardButton("расписание на завтра", callback_data="next_day")]]
	inlinekbd1 = [[InlineKeyboardButton("расписание на сегодня", callback_data="today")]]	
	if day == date:
		kbd_markup = InlineKeyboardMarkup(inlinekbd)
	elif day == next_day:
		kbd_markup = InlineKeyboardMarkup(inlinekbd1)
	return kbd_markup


def inline_button_pressed(bot,update):
	query = update.callback_query	
	data = query.data
	if data == "next_day":
		link = (url_times + "day_view/" + next_day + "/")		
	elif data == "today":
		link = (url_times + "day_view/" + date + "/")		
	text = get_times(link)	
	bot.edit_message_text(text = text, chat_id = query.message.chat.id,
		message_id = query.message.message_id,parse_mode = ParseMode.HTML,reply_markup = show_inline(bot,update))


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
	time.sleep(1)
	resp = requests.get(url).text
	soup = BeautifulSoup(resp, "html.parser")	
	s = soup.find("div", class_=("cinema-header__map"))		
	img = s.find("img", class_ = ("image-partial-component","image-partial-component_loaded"))["src"]	
	f = open("images/foto.jpg", "wb")
	r = requests.get(img)
	f.write(r.content)
	f.close()


def show_ten(bot,update,user_data):
	r = requests.get("https://www.kinopoisk.ru/comingsoon/sex/all/").text	
	soup = BeautifulSoup(r, "html.parser")
	premieres = soup.find("div", class_ ="coming_films")
	films = premieres.find_all("div", class_="item")
	count = 0
	result = []
	rusul = ""
	c = 0	
	for film in films:			
		info = film.find_all("div", class_="info")
		for inf in info:			
			title = inf.find_all("div", class_="name")
			for tit in title:					
				name_t = tit.find_all("a", href = re.compile("^/film/"))					
				for nt in name_t:												
					result.append(nt.text)
					a_link =(nt["href"])
					global dict_waiting
					name_title = nt.text.replace("\xa0", " ")
					dict_waiting[name_title] = a_link						
	reply_keyboard = create_buttons(result[0:10])	
	res = (result)
	print(dict_waiting)	
	a=str(res[0:11])
	update.message.reply_text("здесь будет описание..)", reply_markup = ReplyKeyboardMarkup(reply_keyboard,
		resize_keyboard=True))
	return ("waiting")
	

def show_waiting(bot, update,user_data):
	print(dict_waiting)
	user_text = update.message.text
	print(user_text)
	a = dict_waiting.get(user_text)
	url = "https://www.kinopoisk.ru" + str(a)
	time.sleep(1)	
	r = requests.get(url).text
	soup = BeautifulSoup(r,"html.parser")	
	discr = soup.find("div",class_=("brand_words","film-synopsys"), itemprop ="description")
	print(discr.text)
	get_poster(url)
	bot.send_photo(chat_id = update.message.chat_id, photo = open("images/poster.jpg","rb"))
	update.message.reply_text(discr.text)


def get_poster(url):
	r = requests.get(url).text
	soup = BeautifulSoup(r, "html.parser")
	img = soup.find("a", class_ = "popupBigImage")
	poster = img.find("img")["src"]
	f = open("images/poster.jpg", "wb")
	result = requests.get(poster)
	f.write(result.content)
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
	# show_ten()
	# g()
	get_poster("https://www.kinopoisk.ru/film/1047883/")
	
