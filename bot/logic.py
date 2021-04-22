from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
import re, requests

BASE_URL = 'http://localhost:5000'

# Callback data
next, back, searching, brand, engine_volume, engine_type, class_moto, birth_year, gear_type, search, search_all, back_menu = range(12)

#Filter variables
SELECT_BRAND = set()

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
    brands = InlineKeyboardButton('марка', callback_data=str(brand))
    type_engine = InlineKeyboardButton('впрыск и кубатура', callback_data=str(engine_type))
    motocycle_class = InlineKeyboardButton('класс', callback_data=str(class_moto))
    year_birth = InlineKeyboardButton('год выпуска', callback_data=str(birth_year))
    type_gear = InlineKeyboardButton('тип передачи', callback_data=str(gear_type))
    start_search = InlineKeyboardButton('поиск', callback_data=str(search))
    keyboard.append([brands, type_engine])
    keyboard.append([motocycle_class, year_birth, type_gear])
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
    search = InlineKeyboardButton('поиск', callback_data=str(f'search'))
    next_button = InlineKeyboardButton('вперед>>', callback_data=str(next))
    back_to_menu = InlineKeyboardButton('назад к меню', callback_data=str(back_menu))
    searchALL = InlineKeyboardButton('поиск по всем', callback_data=str(search_all))
    keyboard.append(search_keyboard(update, context))
    keyboard.append([back_button, search, next_button])
    keyboard.append([searchALL, back_to_menu])
    return keyboard


def search_keyboard(update, context):
    brands_list = context.user_data['brands_list']
    brand_index = context.user_data['brand_index']
    row = []
    keyboard = []
    if brand_index == None:
        for brand_index in range(3):
            row.append(InlineKeyboardButton(brands_list[brand_index], callback_data=(f"brand|{brands_list[brand_index]}")))
        context.user_data['brand_index'] = 0
        return row
    else:
        for i in range(brand_index, brand_index + 3):
            row.append(InlineKeyboardButton(brands_list[i], callback_data=(f"brand|{brands_list[i]}")))
        keyboard.append(row)
        return row


def next_brand(update, context):
    query = update.callback_query
    query.answer()
    index = context.user_data['brand_index']
    brands_list = context.user_data['brands_list']
    if (index + 3) <= len(brands_list):
        context.user_data['brand_index'] = index + 3
    else:
        context.user_data['brand_index'] = len(brands_list) - 3
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


def new_keyboard(update, context, keyboard):
    query = update.callback_query
    return query.edit_message_text(f'Выберите один из брендов', reply_markup=InlineKeyboardMarkup(keyboard))


def button_filter(update, context):
    query = update.callback_query
    selected_button = query['data'].split('|')
    if selected_button[0] == 'brand':
        SELECT_BRAND.add(selected_button[1])
    context.user_data['filter_by_brand'] = SELECT_BRAND


def type_engine(update, context):
    keyboard = []
    carburator = InlineKeyboardButton('карбюратор', callback_data=str(f'carburator'))
    injector = InlineKeyboardButton('инжектор', callback_data=str(f'injector'))
    less_125 = InlineKeyboardButton('<125', callback_data=str(f'less_125'))
    less_400 = InlineKeyboardButton('<400', callback_data=str(f'less_400'))
    less_999 = InlineKeyboardButton('<999', callback_data=str(f'less_999'))
    more_liter = InlineKeyboardButton('1000>', callback_data=str(f'liter'))
    search = InlineKeyboardButton('поиск', callback_data=str(f'search'))
    back_to_menu = InlineKeyboardButton('назад к меню', callback_data=str(back_menu))
    keyboard.append([carburator, injector])
    keyboard.append([less_125, less_400, less_999, more_liter])
    keyboard.append([search, back_to_menu])
    query = update.callback_query
    return query.edit_message_text(f'Выберите тип двигателя и объем', reply_markup=InlineKeyboardMarkup(keyboard))


def backword_to_menu(update, context):
    keyboard = main_keyboard()
    query = update.callback_query
    return query.edit_message_text(f' Выберите необходимый тип фильтра ', reply_markup=InlineKeyboardMarkup(keyboard))


def gears_button(update, context):
    keyboard = []
    belt = InlineKeyboardButton('ремень', callback_data=str(f'belt'))
    chain = InlineKeyboardButton('цепь', callback_data=str(f'chain'))
    shaft = InlineKeyboardButton('кардан', callback_data=str(f'shaft'))
    search = InlineKeyboardButton('поиск', callback_data=str(f'search'))
    back_to_menu = InlineKeyboardButton('назад к меню', callback_data=str(back_menu))
    keyboard.append([belt, chain, shaft])
    keyboard.append([search, back_to_menu])
    query = update.callback_query
    return query.edit_message_text(f'Выберите тип передачи', reply_markup=InlineKeyboardMarkup(keyboard))


def moto_class(update, context):
    keyboard = []
    sport = InlineKeyboardButton('sport', callback_data=str(f'sport'))
    classiс = InlineKeyboardButton('classiс', callback_data=str(f'classiс'))
    back_to_menu = InlineKeyboardButton('назад к меню', callback_data=str(back_menu))
    keyboard.append([sport, classiс])
    keyboard.append([back_to_menu])
    query = update.callback_query
    return query.edit_message_text('class motocycle', reply_markup=InlineKeyboardMarkup(keyboard))