import logging

import settings
from handlers import *
from citie import *
from telegram import KeyboardButton

from telegram.ext import Updater, CommandHandler, MessageHandler, \
    Filters, RegexHandler, ConversationHandler, CallbackQueryHandler

logging.basicConfig(format = "%(name)s - %(levelname)s - %(message)s",
                    level = logging.INFO,
                    filename = "bot.log")

location_button = KeyboardButton("определить по месту нахождения", request_location=True)
cities = "к списку городов"

def main():
    
    mybot = Updater(settings.API_KEY, request_kwargs=settings.PROXY)
    logging.info("starting") 
    dp = mybot.dispatcher  
   
    dp.add_handler(CommandHandler("start", greet_user,pass_user_data=True))
    dp.add_handler(CommandHandler("cancel", stop_conv_hand,pass_user_data=True))
    dp.add_handler(RegexHandler("^(start)$", greet_user,pass_user_data=True))    
    dp.add_handler(RegexHandler("^(поменять смайлик)$", change_ava, pass_user_data = True))  
    dp.add_handler(CallbackQueryHandler(inline_button_pressed))  

    kino_dialog = ConversationHandler(
        entry_points = [RegexHandler("^(выбрать город)$", k_select_city,
            pass_user_data=True)],
        states = {
            "in_start":[MessageHandler(Filters.text, greet_user, pass_user_data= True )],
            "select_city":[MessageHandler(Filters.text, k_select_city, pass_user_data= True )],
            "select_cinema":[MessageHandler(Filters.text, get_list_kinoteatr, pass_user_data= True )],
            "select_film":[MessageHandler(Filters.text, kino_details, pass_user_data= True )],
            "show":[MessageHandler(Filters.text, get_times, pass_user_data= True )]            
        },
        fallbacks =[] #[MessageHandler(Filters.text , dontknow)]
    )

    dp.add_handler(kino_dialog)    
    dp.add_handler(MessageHandler(Filters.text, talk_to_me, pass_user_data=True))
    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()




