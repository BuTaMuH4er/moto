from api.config import API_KEY_BOT
import logging, logic
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters, CallbackQueryHandler
from datetime import datetime


logging.basicConfig(filename='bot.log', level=logging.INFO)

# Callback data
next, back, searching, brand, engine_volume, engine_type, class_moto, birth_year, type_gear, search_start = range(10)


if __name__ == '__main__':
    mybot = Updater(API_KEY_BOT, use_context=True)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', logic.start_bot, pass_user_data=True))
    dp.add_handler(CallbackQueryHandler(logic.brands, pass_user_data=True, pattern='^' + str(brand) + '$'))
    dp.add_handler(CallbackQueryHandler(logic.next_brand, pass_user_data=True, pattern='^' + str(next) + '$'))
    dp.add_handler(CallbackQueryHandler(logic.back_brand, pass_user_data=True, pattern='^' + str(back) + '$'))

    time_now = datetime.today().strftime("%H:%M:%S  %d/%m/%Y")
    logging.info(f'{time_now} Бот стартовал')
    mybot.start_polling()
    mybot.idle()
