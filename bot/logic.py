from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
import re, requests
from api.model import Motocycle

BASE_URL = 'http://localhost:5000'

# Callback data
next, back, searching, brand, engine_volume, engine_type, class_moto, birth_year, gear_type, search, search_all, back_menu = range(12)

#Filter variables
SELECT_BRAND = set()                #context.user_data['filter_by_brand']
SELECT_GEAR = set()                 #context.user_data['selected_gear']
SELECT_ENGINE_TYPE = set()          #context.user_data['engine_type']
SELECT_ENGINE_SIZE = set()          #context.user_data['engine_size']
#context.user_data['list_motos_class']


def start_bot(update, context):
    #This function starts bot and call main keyboard
    dict_brands = requests.get(BASE_URL + '/brands').json()
    brands_list = list(dict_brands.keys())
    context.user_data['brands_list'] = brands_list
    update.message.reply_text('Привет. Я wiki бот по мотоциклам. \n'
                              'Ты можешь посмотреть краткую справочную информацию по моделям мотоциклов. \n'
                              )
    keyboard = main_keyboard()
    update.message.reply_text(f' Выберите необходимый тип фильтра ', reply_markup=InlineKeyboardMarkup(keyboard))
    context.user_data['list_motos_class'] = [i.cycle_class for i in (Motocycle.query.distinct(Motocycle.cycle_class).all())] #необходимо для генерации кнопок из списка существующих классов мотоциклов на момент запуска бота



def main_keyboard():
    #this function generate main keyboard with all filters
    keyboard = []
    brands = InlineKeyboardButton('марка', callback_data=str(brand))
    type_engine = InlineKeyboardButton('впрыск и кубатура', callback_data=str(engine_type))
    motocycle_class = InlineKeyboardButton('класс', callback_data=str(class_moto))
    year_birth = InlineKeyboardButton('год выпуска', callback_data=str(birth_year))
    type_gear = InlineKeyboardButton('тип передачи', callback_data=str(gear_type))
    start_search = InlineKeyboardButton('поиск', callback_data=str(search))
    clear_filter = InlineKeyboardButton('сбросить фильтры', callback_data='filter_0')
    keyboard.append([brands, type_engine])
    keyboard.append([motocycle_class, year_birth, type_gear])
    keyboard.append([start_search, clear_filter])
    return keyboard


def clear_filter(update, context):
    context.user_data['selected_gear'] = SELECT_GEAR.clear()
    context.user_data['engine_size'] = SELECT_ENGINE_SIZE.clear()
    context.user_data['engine_type'] = SELECT_ENGINE_TYPE.clear()
    context.user_data['filter_by_brand'] = SELECT_BRAND.clear()

def brands(update, context):
    keyboard = brands_nav(update, context)
    query = update.callback_query
    query.edit_message_text(f'Выберите один из брендов', reply_markup=InlineKeyboardMarkup(keyboard))


def brands_nav(update, context):
    #this function generate keyboard with filter by brand
    keyboard = []
    try:
        context.user_data['brand_index']
    except KeyError:
        context.user_data['brand_index'] = None
    #buttons for 2nd row buttons
    back_button = InlineKeyboardButton('<<назад', callback_data=str(back))
    start_search = InlineKeyboardButton('поиск', callback_data=str(search))
    next_button = InlineKeyboardButton('вперед>>', callback_data=str(next))
    back_to_menu = InlineKeyboardButton('назад к меню', callback_data=str(back_menu))
    searchALL = InlineKeyboardButton('поиск по всем', callback_data=str(search_all))
    keyboard.append(search_keyboard(update, context))
    keyboard.append([back_button, start_search, next_button])
    keyboard.append([searchALL, back_to_menu])
    return keyboard


def search_keyboard(update, context):
    #function generate row buttons with three brand names
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
    #call button NEXT to show next brands in list for filter by brand name
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
    # call button BACK to show previous brands in list for filter by brand name
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
    #function add to user_data brand name when you choose brand in filter
    query = update.callback_query
    selected_button = query['data'].split('|')
    if selected_button[0] == 'brand':
        if selected_button[1] in SELECT_BRAND:
            SELECT_BRAND.remove(selected_button[1])
        else:
            SELECT_BRAND.add(selected_button[1])
    context.user_data['filter_by_brand'] = SELECT_BRAND


def type_engine(update, context):
    #function generate keyboard with filter by engines
    keyboard = []
    carburator= InlineKeyboardButton('карбюратор', callback_data=str(f'carburetor'))
    injector = InlineKeyboardButton('инжектор', callback_data=str(f'injection'))
    less_125 = InlineKeyboardButton('<125', callback_data=str(f'125'))
    less_400 = InlineKeyboardButton('<400', callback_data=str(f'400'))
    less_999 = InlineKeyboardButton('<999', callback_data=str(f'999'))
    more_liter = InlineKeyboardButton('1000>', callback_data=str(f'liter'))
    start_search = InlineKeyboardButton('поиск', callback_data=str(search))
    back_to_menu = InlineKeyboardButton('назад к меню', callback_data=str(back_menu))
    keyboard.append([carburator, injector])
    keyboard.append([less_125, less_400, less_999, more_liter])
    keyboard.append([start_search, back_to_menu])
    query = update.callback_query
    return query.edit_message_text(f'Выберите тип двигателя и объем', reply_markup=InlineKeyboardMarkup(keyboard))


def select_engine_size(update, context):
    query = update.callback_query
    if query['data'] in SELECT_ENGINE_SIZE:
        SELECT_ENGINE_SIZE.remove(query['data'])
    else:
        SELECT_ENGINE_SIZE.add(query['data'])
    context.user_data['engine_size'] = SELECT_ENGINE_SIZE


def select_type_engine(update, context):
    query = update.callback_query
    if query['data'] in SELECT_ENGINE_TYPE:
        SELECT_ENGINE_TYPE.remove(query['data'])
    else:
        SELECT_ENGINE_TYPE.add(query['data'])
    context.user_data['engine_type'] = SELECT_ENGINE_TYPE


def backword_to_menu(update, context):
    #callback previous keyboard menu
    keyboard = main_keyboard()
    query = update.callback_query
    return query.edit_message_text(f' Выберите необходимый тип фильтра ', reply_markup=InlineKeyboardMarkup(keyboard))


def gears_button(update, context):
    #function generate keyboard with filter by gear type
    keyboard = []
    belt_button = InlineKeyboardButton('ремень', callback_data='belt')
    chain_button = InlineKeyboardButton('цепь', callback_data='chain')
    shaft_button = InlineKeyboardButton('кардан', callback_data='shaft')
    start_search = InlineKeyboardButton('поиск', callback_data=str(search))
    back_to_menu = InlineKeyboardButton('назад к меню', callback_data=str(back_menu))
    keyboard.append([shaft_button, chain_button, belt_button])
    keyboard.append([start_search, back_to_menu])
    query = update.callback_query
    query.edit_message_text(f'Выберите тип передачи', reply_markup=InlineKeyboardMarkup(keyboard))
    #return query.edit_message_text(f'Выберите тип передачи', reply_markup=InlineKeyboardMarkup(keyboard))


def selected_gear_type(update, context):
    query = update.callback_query
    if query['data'] in SELECT_GEAR:
        SELECT_GEAR.remove(query['data'])
    else:
        SELECT_GEAR.add(query['data'])
    context.user_data['selected_gear'] = SELECT_GEAR


def moto_class_buttons(update, context):
    buttons_row = []
    try:
        context.user_data['class_index']
    except KeyError:
        context.user_data['class_index'] = 0
    motocycle_class = context.user_data['list_motos_class']
    if context.user_data['class_index'] == 0:
        for i in range(3):
            buttons_row.append(InlineKeyboardButton(motocycle_class[i], callback_data=(f'class|{motocycle_class[i]}')))
    else:
        class_index = context.user_data['class_index']
        for i in range(class_index, class_index+3):
            buttons_row.append(InlineKeyboardButton(motocycle_class[i], callback_data=(f'class|{motocycle_class[i]}')))
    return buttons_row


def listing_moto_class(update, context):
    query = update.callback_query
    query.answer()
    class_index = context.user_data['class_index']
    selected_button = query['data']
    if 'back_class_motocycle' in selected_button:
        class_index -= 3
        if class_index < 0:
            class_index = 0
        context.user_data['class_index'] = class_index
    if 'next_class_motocycle' in selected_button:
        class_index += 3
        if class_index > len(context.user_data['list_motos_class']):
            class_index = len(context.user_data['list_motos_class']) - 3
    context.user_data['class_index'] = class_index
    moto_class(update, context)


def moto_class(update, context):
    keyboard = []
    row = moto_class_buttons(update, context)
    back_to_menu = InlineKeyboardButton('назад к меню', callback_data=str(back_menu))
    back_button = InlineKeyboardButton('<<назад', callback_data='back_class_motocycle')
    next_button = InlineKeyboardButton('вперед>>', callback_data='next_class_motocycle')
    start_search = InlineKeyboardButton('поиск', callback_data=str(search))
    keyboard.append(row)
    keyboard.append([back_button, start_search, next_button])
    keyboard.append([back_to_menu])
    query = update.callback_query
    return query.edit_message_text('Выберите класс мотоцикла.', reply_markup=InlineKeyboardMarkup(keyboard))


def filter_list(update, context):
    list_ids = []
    # возвращает обратно множество id мотоциклов для дальнейшей фильтрации
    print(f'ПОИСК нажат')
    print(f'Проверить контекст')
    #print(f'filter_list по передаче {context.user_data["selected_gear"]}')
    #print(f'filter_list по бренду {context.user_data["filter_by_brand"]}')
    print(f'фильтр по типу двигателя {context.user_data["engine_type"]}')
    print(f'фильтр по кубатуре {context.user_data["engine_size"]}')
    filter_by_brand = set()
    filter_by_gear = set()
    filter_by_engine_type = set()
    filter_by_engine_size = set()
    if context.user_data['filter_by_brand']:
        dict_brands = requests.get(BASE_URL + '/brands').json()
        for brand in context.user_data['filter_by_brand']:
            brand_id = dict_brands[brand]
            for i in list(requests.get(BASE_URL + '/by_brand/' + str(brand_id)).json().keys()) : filter_by_brand.add(i)
        print(f'Длина списка по маркам {len(filter_by_brand)}')

    if context.user_data['selected_gear']:
        for gear_type in context.user_data['selected_gear']:
            for i in list(requests.get(BASE_URL + '/by_gear_type/' + str(gear_type)).json().keys()) : filter_by_gear.add(i)
        print(f'Длина списка по передачам {len(filter_by_gear)}')

    if context.user_data['engine_type']:
        for engine in context.user_data['engine_type']:
            for i in list(requests.get(BASE_URL + '/engine_type/' + str(engine)).json().keys()) : filter_by_engine_type.add(i)
        print(f'Длина списка типу впрыска {len(filter_by_engine_type)}')

    if context.user_data['engine_size']:
        for engine in context.user_data['engine_size']:
            for i in list(requests.get(BASE_URL + '/engine/' + str(engine)).json().keys()) : filter_by_engine_size.add(i)
        print(f'Длина списка кубатуре {len(filter_by_engine_size)}')

    filters = [filter_by_engine_type, filter_by_engine_size, filter_by_gear, filter_by_brand]
    for filter in filters:
        if len(list_ids) == 0:
            list_ids = filter
        elif len(filter) != 0:
            list_ids = list_ids.intersection(list(filter))
    print(f'длина конечного списка после фильтров: {len(list_ids)}')
    return list_ids

#вероятно необходимо в каждом подменю делать сброс конкретного фильтра