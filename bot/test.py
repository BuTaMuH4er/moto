from api.config import API_KEY_BOT
import logging, requests
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import datetime, logic
from datetime import datetime


logging.basicConfig(filename='bot.log', level=logging.INFO)

BASE_URL = 'http://localhost:5000'
motos = {'Honda': '1',
         'Yamaha': '2',
         'Harley': '3',
         'Suzuki': '4',
         'Viktory': '5',
         'BMW': '6',
         'KTM': '7',
         'Baja': '8',
         'Indian': '9',
         'Triumph': '10'}


def brands_buttons(index_button):
    list_brands = list(motos.keys())
    a = list_brands[index_button:index_button + 3]
    return a


def key_list(update, context):
    row = []
    keyboard = []
    for button in brands_buttons(0):
        row.append(InlineKeyboardButton(button, callback_data=str(button)))
    keyboard.append(row)
    row = []
    back_button = InlineKeyboardButton('<<назад', callback_data=str('back'))
    search = InlineKeyboardButton('поиск', callback_data=str('search'))
    next_button = InlineKeyboardButton('вперед>>', callback_data=str('next'))
    row.append(back_button)
    row.append(search)
    row.append(next_button)
    keyboard.append(row)
    keyboard.append([InlineKeyboardButton('поиск по всем', callback_data=str('all'))])
    update.message.reply_text(f'Поиск по брендам', reply_markup=InlineKeyboardMarkup(keyboard))


def search_keyboard(brand_index=None, next=False, back=False):
    row = []
    keyboard = []
    dict_brands = requests.get(BASE_URL+'/brands').json()
    brands_list = list(dict_brands.keys())
    if brand_index==None:
        for brand_index in range(3):
            row.append(InlineKeyboardButton(brands_list[brand_index]), callback_data=str(brands_list[brand_index]))
        return keyboard.append(row)
    elif (brand_index+3) <= len(brands_list) and next==True:
        for i in range(brands_list, brands_list+3):
            row.append(InlineKeyboardButton(brands_list[i]), callback_data=str(brands_list[i]))
        return keyboard.append(row)
    elif (brand_index+3) > len(brands_list) and next==True:
        ####тут просто можно написать генератор, вероятно и в других случаях, генератор списка кнопок
        for i in range(brand_index, len(brands_list)):
            row.append(InlineKeyboardButton(brands_list[i]), callback_data=str(brands_list[i]))
        return keyboard.append(row)
    elif (brand_index-3) >= 0 and back==True:
        x = brand_index-3
        for i in range(x, brands_list):
            row.append(InlineKeyboardButton(brands_list[i]), callback_data=str(brands_list[i]))
        return keyboard.append(row)
    elif (brand_index-3) < 0 and back==True:
        for i in range(brand_index):
            row.append(InlineKeyboardButton(brands_list[i]), callback_data=str(brands_list[i]))
        return keyboard.append(row)




#TODO: Необходимо создать цикл для выгрузки названий кнопок и их выбора. Создать функции перелистывания.
#вероятно эти функции должны получать на входе список и положение в меню.

if __name__ == '__main__':
    mybot = Updater(API_KEY_BOT, use_context=True)



    dp = mybot.dispatcher
    index_button = 0
    dp.add_handler(CommandHandler('start', key_list))
    dp.add_handler(CommandHandler('next', key_list))

    time_now = datetime.today().strftime("%H:%M:%S  %d/%m/%Y")
    logging.info(f'{time_now} Бот стартовал')
    mybot.start_polling()
    mybot.idle()