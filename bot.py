import logging

import settings
from handlers import *

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler

logging.basicConfig(format = "%(name)s - %(levelname)s - %(message)s",
                    level = logging.INFO,
                    filename = "bot.log")


def main():
    mybot = Updater(settings.API_KEY, request_kwargs=settings.PROXY)
    logging.info("starting")    

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user,pass_user_data=True))
    dp.add_handler(RegexHandler("^(start)$", greet_user,pass_user_data=True))
    dp.add_handler(RegexHandler("^(ава)$", change_ava, pass_user_data = True))
    
    kino_dialog = ConversationHandler(
        entry_points = [RegexHandler("^(выбрать город)$", k_select_city,
            pass_user_data=True)],
        states = {
            "select_city":[MessageHandler(Filters.text, k_select_cinema, pass_user_data= True )],
            "select_cinema":[MessageHandler(Filters.text, k_select_cinema, pass_user_data= True )]
        },
        fallbacks = []
    )
    dp.add_handler(kino_dialog)

    dp.add_handler(MessageHandler(Filters.text, talk_to_me, pass_user_data=True))


    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()






# a = {"f":4, "d":6, "h":9}
# def item_in_dict(items_):
#     for item_ in items_:
#         return(item_)
        
# print([item_in_dict(a)])