from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
import requests

BASE_URL = 'http://localhost:5000'

# Callback data
next, back, searching, brand, engine_volume, engine_type, class_moto, birth_year, type_gear, search_start = range(10)


def start_bot(update, context):
    dict_brands = requests.get(BASE_URL + '/brands').json()
    brands_list = list(dict_brands.keys())
    context.user_data['brands_list'] = brands_list
    update.message.reply_text('Привет. Я wiki бот по мотоциклам. \n'
                              'Ты можешь посмотреть краткую справочную информацию по моделям мотоциклов. \n'
                              )
    keyboard = main_keyboard()
    update.message.reply_text(f' Выберите необходимый тип фильтра ', reply_markup=InlineKeyboardMarkup(keyboard))


def main_keyboard():
    #this function generate main keyboard with all filters
    keyboard = []
    brands = InlineKeyboardButton('производитель', callback_data=str(brand))
    engine = InlineKeyboardButton('кубатура', callback_data=str(engine_volume))
    type_engine = InlineKeyboardButton('впрыск', callback_data=str(engine_type))
    motocycle_class = InlineKeyboardButton('класс', callback_data=str(class_moto))
    year_birth = InlineKeyboardButton('год выпуска', callback_data=(birth_year))
    gear_type = InlineKeyboardButton('тип передачи', callback_data=(type_gear))
    start_search = InlineKeyboardButton('поиск', callback_data=(search_start))
    keyboard.append([brands, engine, type_engine])
    keyboard.append([motocycle_class, year_birth, gear_type])
    keyboard.append([start_search])
    return keyboard


def brands(update, context):
    keyboard = brands_nav(update, context)
    query = update.callback_query
    query.edit_message_text(f'Выберите один из брендов', reply_markup=InlineKeyboardMarkup(keyboard))


def brands_nav(update, context):
    keyboard = []
    try:
        context.user_data['brand_index']
    except KeyError:
        context.user_data['brand_index'] = None
    #buttons for 2nd row buttons
    back_button = InlineKeyboardButton('<<назад', callback_data=str(back))
    search = InlineKeyboardButton('поиск', callback_data=str(searching))
    next_button = InlineKeyboardButton('вперед>>', callback_data=str(next))
    keyboard.append(search_keyboard(update, context))
    keyboard.append([back_button, search, next_button])
    keyboard.append([InlineKeyboardButton('поиск по всем', callback_data=str('all'))])
    return keyboard


def search_keyboard(update, context):
    brands_list = context.user_data['brands_list']
    brand_index = context.user_data['brand_index']
    row = []
    keyboard = []
    if brand_index == None:
        for brand_index in range(3):
            row.append(InlineKeyboardButton(brands_list[brand_index], callback_data=str(brands_list[brand_index])))
        context.user_data['brand_index'] = 0
        return row
    else:
        for i in range(brand_index, brand_index + 3):
            row.append(InlineKeyboardButton(brands_list[i], callback_data=str(brands_list[i])))
        keyboard.append(row)
        return row


def next_brand(update, context):
    print(f'Старт кнопки next')
    query = update.callback_query
    query.answer()
    index = context.user_data['brand_index']
    brands_list = context.user_data['brands_list']
    if (index + 3) <= len(brands_list):
        context.user_data['brand_index'] = index + 3
    else:
        context.user_data['brand_index'] = len(brans_list) - 3
    keyboard = brands_nav(update, context)
    new_keyboard(update, context, keyboard)

#из функций переключения по списку мы передаем бренд_индекс через юзер_дата, дальше сравниваем какое значение
#у бренд индекса и исходя из этого передаем значения в серч_кейбор и делаем кнопки

def back_brand(update, context):
    query = update.callback_query
    query.answer()
    index = context.user_data['brand_index']
    if (index - 3) >= 0:
        context.user_data['brand_index'] = index - 3
    else:
        context.user_data['brand_index'] = 0
    keyboard = brands_nav(update, context)
    new_keyboard(update, context, keyboard)


def searching(update, context):
    print(f'Нажали на кнопку поиска')


def new_keyboard(update, context, keyboard):
    query = update.callback_query
    return query.edit_message_text(f'Выберите один из брендов', reply_markup=InlineKeyboardMarkup(keyboard))

