from api.config import API_KEY_BOT
import logging
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
import datetime, logic
from datetime import datetime


logging.basicConfig(filename='bot.log', level=logging.INFO)


SEARCH, FILTER_BRAND = range(2)



if __name__ == '__main__':
    mybot = Updater(API_KEY_BOT, use_context=True)
    conv_hand = ConversationHandler(
        entry_points=[CommandHandler('start', logic.start_bot)],
        states={
            SEARCH: [MessageHandler(Filters.text, logic.search_keyboard)],
        },
        fallbacks=[CommandHandler('stop', logic.stop)],
    )

    dp = mybot.dispatcher
    dp.add_handler(conv_hand)

    time_now = datetime.today().strftime("%H:%M:%S  %d/%m/%Y")
    logging.info(f'{time_now} Бот стартовал')
    mybot.start_polling()
    mybot.idle()
