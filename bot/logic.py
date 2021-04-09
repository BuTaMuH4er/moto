from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import requests

BASE_URL = 'http://localhost:5000'

SEARCH = range(1)

def brands_nav():
    keyboard = []
    #buttons for 2nd row buttons
    back_button = InlineKeyboardButton('<<назад', callback_data=str('back'))
    search = InlineKeyboardButton('поиск', callback_data=str('search'))
    next_button = InlineKeyboardButton('вперед>>', callback_data=str('next'))
    keyboard.append([InlineKeyboardButton('поиск по всем', callback_data=str('all'))])
    keyboard.append([back_button, search, next_button])
    return keyboard

def start_bot(update, context):
    update.message.reply_text('Привет. Я wiki бот по мотоциклам. \n'
                              'Ты можешь посмотреть краткую справочную информацию по моделям мотоциклов. \n'
                              )
    keyboard_brands = brands_nav()
    #brands =
    update.message.reply_text(f'Выберите один из брендов', reply_markup=InlineKeyboardMarkup(keyboard_brands))
    return SEARCH


def search_keyboard(brand_id=None):
    dict_brands = requests.get(BASE_URL+'/brands').json()
"""    if brand_id==None:
        for i in dict_brands.item:"""


#def search_by(brand=None, birth_year=None, model=None, engine=None):
#    url_brands = BASE_URL+'/by_brand/'+ brand
#    #url_by_id = BASE_URL+'/'+str(67)
#    result = requests.get(url_brands)
#    print(result.json())


def stop(update, context):
    update.message.reply_text(f'Досвидания')
    return ConversationHandler.END


#if __name__ == '__main__':
#   search_keyboard()