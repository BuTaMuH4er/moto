from api.config import API_KEY_BOT
import logging
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
import datetime, logic
from datetime import datetime


logging.basicConfig(filename='bot.log', level=logging.INFO)

#Stages
SEARCH, FILTER_BRAND = range(2)
# Callback data
next, back, searching = range(3)




if __name__ == '__main__':
    mybot = Updater(API_KEY_BOT, use_context=True)
    conv_hand = ConversationHandler(per_message=False,
        entry_points=[CommandHandler('start', logic.start_bot, pass_user_data=True)],
        states={
            SEARCH: [
                MessageHandler(Filters.text, logic.search_keyboard, pass_user_data=True),
            CallbackQueryHandler(logic.next_brand, pass_user_data=True, pattern='^' + str(next) + '$'),
            CallbackQueryHandler(logic.back_brand, pass_user_data=True, pattern='^' + str(back) + '$'),
            CallbackQueryHandler(logic.searching, pattern='^' + str(searching) + '$'),
            ],
        },
        fallbacks=[CommandHandler('stop', logic.stop)],
    )

    dp = mybot.dispatcher
    dp.add_handler(conv_hand)

    time_now = datetime.today().strftime("%H:%M:%S  %d/%m/%Y")
    logging.info(f'{time_now} Бот стартовал')
    mybot.start_polling()
    mybot.idle()
