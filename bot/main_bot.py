from api.config import API_KEY_BOT
import logging, logic
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters, CallbackQueryHandler
from datetime import datetime


logging.basicConfig(filename='bot.log', level=logging.INFO)

# Callback data
next, back, searching, brand, engine_volume, engine_type, class_moto, birth_year, gear_type, search, search_all, back_menu = range(12)


if __name__ == '__main__':
    mybot = Updater(API_KEY_BOT, use_context=True)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', logic.start_bot, pass_user_data=True))
    dp.add_handler(CallbackQueryHandler(logic.clear_filter, pass_user_data=True, pattern='^' + 'filter_0' + '$'))
    dp.add_handler(CallbackQueryHandler(logic.brands, pass_user_data=True, pattern='^' + str(brand) + '$'))
    dp.add_handler(CallbackQueryHandler(logic.next_brand, pass_user_data=True, pattern='^' + str(next) + '$'))
    dp.add_handler(CallbackQueryHandler(logic.back_brand, pass_user_data=True, pattern='^' + str(back) + '$'))
    dp.add_handler(CallbackQueryHandler(logic.type_engine, pass_user_data=True, pattern='^' + str(engine_type) + '$'))
    dp.add_handler(CallbackQueryHandler(logic.backword_to_menu, pass_user_data=True, pattern='^' + str(back_menu) + '$'))
    dp.add_handler(CallbackQueryHandler(logic.gears_button, pass_user_data=True, pattern='^' + str(gear_type) + '$'))
    dp.add_handler(CallbackQueryHandler(logic.moto_class, pass_user_data=True, pattern='^' + str(class_moto) + '$'))
    #dp.add_handler(CallbackQueryHandler(logic.filter_list, pass_user_data=True, pattern='^' + str(search) + '$'))
    dp.add_handler(CallbackQueryHandler(logic.show_list_motocycles, pass_user_data=True, pattern='^' + str(search) + '$'))
    dp.add_handler(CallbackQueryHandler(logic.select_type_engine, pass_user_data=True, pattern='^' + 'carburetor|injection' + '$'))
    dp.add_handler(CallbackQueryHandler(logic.select_engine_size, pass_user_data=True, pattern='^' + '125|400|999|liter' + '$'))
    dp.add_handler(CallbackQueryHandler(logic.selected_gear_type, pass_user_data=True, pattern='^' + 'shaft|belt|chain' + '$'))
    dp.add_handler(CallbackQueryHandler(logic.listing_moto_class, pass_user_data=True, pattern='^' + 'back_class_motocycle|next_class_motocycle' + '$'))


    dp.add_handler(CallbackQueryHandler(logic.button_filter, pass_user_data=True, pattern='^[brand|class]'))



    time_now = datetime.today().strftime("%H:%M:%S  %d/%m/%Y")
    logging.info(f'{time_now} Бот стартовал')
    mybot.start_polling()
    mybot.idle()
