from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
import requests

BASE_URL = 'http://localhost:5000'

SEARCH = range(1)

def brands_nav(update, context):
    keyboard = []
    try:
        brand_index = context.user_data['brand_index']
        print(f'{brand_index} в самом начала брендс нав')
    except KeyError:
        context.user_data['brand_index'] = None
        brand_index = context.user_data['brand_index']
    #buttons for 2nd row buttons
    back_button = InlineKeyboardButton('<<назад', callback_data=str('back'))
    search = InlineKeyboardButton('поиск', callback_data=str('search'))
    next_button = InlineKeyboardButton('вперед>>', callback_data=str('next'))
    if brand_index==None:
        keyboard.append(search_keyboard(update, context))
    else:
        keyboard.append(search_keyboard(brand_index))
    keyboard.append([back_button, search, next_button])
    keyboard.append([InlineKeyboardButton('поиск по всем', callback_data=str('all'))])
    print(f'brands_nav начало функции {brand_index}')
    return keyboard

def start_bot(update, context):
    dict_brands = requests.get(BASE_URL + '/brands').json()
    brands_list = list(dict_brands.keys())
    context.user_data['brands_list'] = brands_list
    update.message.reply_text('Привет. Я wiki бот по мотоциклам. \n'
                              'Ты можешь посмотреть краткую справочную информацию по моделям мотоциклов. \n'
                              )
    keyboard_brands = brands_nav(update, context)
    update.message.reply_text(f'Выберите один из брендов', reply_markup=InlineKeyboardMarkup(keyboard_brands))
    return SEARCH


def search_keyboard(update, context):
    brands_list = context.user_data['brands_list']
    brand_index = context.user_data['brand_index']
    print(f'search_keyboard начало функции {brand_index}')
    row = []
    keyboard = []
    if brand_index == None:
        for brand_index in range(3):
            row.append(InlineKeyboardButton(brands_list[brand_index], callback_data=str(brands_list[brand_index])))
        context.user_data['brand_index'] = 0
        print(f' условия, изменение индекса {context.user_data["brand_index"]}')
        return row
    elif brand_index <= len(brands_list):
        for i in range(brands_list, brands_list + 3):
            row.append(InlineKeyboardButton(brands_list[i], callback_data=str(brands_list[i])))
            context.user_data['brand_index'] = brand_index + 3
        return keyboard.append(row)
    elif brand_index > len(brands_list):
        for i in range(brand_index, len(brands_list)):
            row.append(InlineKeyboardButton(brands_list[i], callback_data=str(brands_list[i])))
        return keyboard.append(row)
    #back
    elif brand_index < 0:
        for i in range(brand_index):
            row.append(InlineKeyboardButton(brands_list[i], callback_data=str(brands_list[i])))
        return keyboard.append(row)


def next_brand(update, context):
    print(f'кто-то запросил следующие бренды')
    query = update.callback_query
    query.answer()
    index = context.user_data['brand_index']
    context.user_data['brand_index'] = index + 3
    return SEARCH

#из функций переключения по списку мы передаем бренд_индекс через юзер_дата, дальше сравниваем какое значение
#у бренд индекса и исходя из этого передаем значения в серч_кейбор и делаем кнопки

def back_brand(update, context):
    query = update.callback_query
    query.answer()
    index = context.user_data['brand_index']
    context.user_data['brand_index'] = index - 3
    return SEARCH


def stop(update, context):
    update.message.reply_text(f'Досвидания')
    return ConversationHandler.END


#if __name__ == '__main__':
#   search_keyboard()