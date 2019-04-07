# -- coding: utf-8 --

from bs4 import BeautifulSoup
import requests
import logging
import re

from telegram import replykeyboardremove, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler


logging.basicConfig(format = "%(name)s - %(levelname)s - %(message)s",
                    level = logging.INFO,
                    filename = "bot.log")

dict_kinoteatr= {}



def get_times(link):	
	
	
	# user_text = update.message.text
	# print(dict_kinoteatr)
	# a = dict_kinoteatr.get(user_text) 
	# print(a)	
	# print(film)
	
	# film = requests.get("https://www.kinopoisk.ru" + str(a))

	r = requests.get(link).text	
	soup = BeautifulSoup(r, "html.parser")	
	print(type(soup))	
	lfs = soup.find_all("div", class_ =("schedule-item"))
	list_films = []
	
	# with open("afisha1.html", "r", encoding = "utf-8") as t:
	# 	text = t.read()
	# 	print(t)
	# 	s = BeautifulSoup(text, "html.parser")		
	# 	lfs = s.find_all("div", class_ =("schedule-item"))
	# 	list_films = []

	for lf in lfs:
		# print(lf.text) #
		lts = lf.find_all("div", class_ =("schedule-film__details"))			
		result = ""
		for lt in lts:
			# print(lt.text)  #film i janre
			dts = lt.find_all("a", class_ = ("link", "schedule-film__title"))				
			dict_titles = {}
			titles = []
			for tit in dts:
				print(tit.text) #film title
				t=tit.text
				result += (t + "\n")
				# update.message.reply_text(t)
				l_gs = lt.find_all("div", class_ = ("schedule-film__summary"))
				d_fs = lf.find_all("span", class_ = ("schedule-item__formats-format"))
				p_ts = lf.find_all("span", class_ = ("schedule-item__session-button-wrapper"))
				list_general = []
				dict_formats = {}
				for lg in l_gs:
					print(lg.text) #details
					lg = lg.text
					result += (lg + "\n")
					# update.message.reply_text(lg)
					list_general.append(lg)
				for df in d_fs:
					print(df.text) #format
					d= df.text
					result += (d + "\n")
					# update.message.reply_text(d)
					time_price = []
					for pt in p_ts:
						print(pt.text) #p_t
						p = pt.text
						result += (p + "\n")
						times = pt.find_all("span", class_ = ("schedule-item__session-button"))
						price = pt.find_all("span", class_ = ("schedule-item__price"))
						for time in times:
							t= (time.text)
						for pric in price:
							p = (pric.text)
						print(t + "- " + p)	
						pr_ti =(t + "- " + p)
						result += (pr_ti + "\n")
						# update.message.reply_text(pr_ti)						
						t = for_in(times)
						p = for_in(price)
						t.extend(p)								
						time_price.append(t)
			print(result)
	return(result)
		# 			dict_formats[d] = time_price
		# 		list_general.append(dict_formats)					
		# 		titles.append(t)				
		# 	list_films.append(list_general)	
		# update.message.reply_text(t)
		# update.message.reply_text(lg)	
		# update.message.reply_text(d)	
		# update.message.reply_text(pr_ti)	


		
def get_kinoteatr():
	r = requests.get("https://www.kinopoisk.ru/cinemas/tc/463/").text	
	soup = BeautifulSoup(r, "html.parser")	
	# name_kinoteatr = soup.find_all("a", class_= "new-list__item-link")
	name_kinoteatr = soup.find_all("a", itemprop= "name")
	links = []	
	cin = []
	links = []
	d = {}
	for once in name_kinoteatr:
		d[once.text] = once.get("href")		
	global dict_kinoteatr
	dict_kinoteatr = d
	return(d)

def get_list_kinoteatr(bot, update, user_data):	
	dict_kinoteatr = get_kinoteatr()
	names_kinoteatr = list(dict_kinoteatr.keys())
	reply_keyboard = create_buttons(names_kinoteatr)
	update.message.reply_text(
        "Отлично! Выбираем",
        reply_markup = ReplyKeyboardMarkup(reply_keyboard, 
        resize_keyboard=True))    
	print(names_kinoteatr)
	print(type(names_kinoteatr))
	print(dict_kinoteatr)
	return("select_film")

def kino_details(bot, update, user_data):
	user_text = update.message.text
	print(user_text)
	print(dict_kinoteatr)
	if user_text in dict_kinoteatr:
		a = dict_kinoteatr.get(user_text) 
		print(a)
		(d) = get_times("https://www.kinopoisk.ru" + str(a))	
		update.message.reply_text(d)
	else:
		update.message.reply_text("unicode-escape")

def create_buttons(list_):
	list_buttons = []
	while len(list_) > 2:
		para_buttons = list_[:2]
		list_buttons.append(para_buttons)        
		list_ = list_[2:]
	list_buttons.append(list_)   
	list_buttons.append(["к списку городов","в начало"])
	return(list_buttons)

			
def for_in(lists):
	d = []
	for list_ in lists:
		d += [(list_.text)]
	return(d)	


if __name__ == "__main__":
	get_times("https://www.kinopoisk.ru/afisha/city/463/cinema/281048/")

	# print(get_times())
	# print(get_kinoteatr())
	# get_list_kinoteatr()

	# a= ["asd","sss","ddd","aaa","qqq","eee","eee"]
	# create_buttons(a)
	# print(get_kinoteatr())

	# get_times("https://www.kinopoisk.ru/afisha/city/463/cinema/280950/day_view/2019-04-07/")
	