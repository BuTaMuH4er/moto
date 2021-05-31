from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from collections import OrderedDict
import requests
from api.model import Motocycle

BASE_URL = 'http://localhost:5000'

# Callback data
next, back, searching, brand, engine_volume, engine_type, class_moto, birth_year, gear_type, search, search_all, back_menu = range(12)

#Filter variables
SELECT_BRAND = set()                #context.user_data['filter_by_brand']
SELECT_GEAR = set()                 #context.user_data['selected_gear']
SELECT_ENGINE_TYPE = set()          #context.user_data['engine_type']
SELECT_ENGINE_SIZE = set()          #context.user_data['engine_size']
SELECT_CLASS_MOTOCYCLE = set()      #context.user_data['selected_motocycle_class']
#context.user_data['list_motos_class']
#context.user_data['index_list_id'] - index in list filtered ids founded motocycles

def start_bot(update, context):
    #This function starts bot and call main keyboard
    dict_brands = requests.get(BASE_URL + '/brands').json()
    brands_list = list(dict_brands.keys())
    context.user_data['brands_list'] = brands_list
    update.message.reply_text('Привет. Я wiki бот по мотоциклам. \n'
                              'Ты можешь посмотреть краткую справочную информацию по моделям мотоциклов. \n'
                              )
    keyboard = main_keyboard()
    update.message.reply_text(f' Выберите необходимый тип фильтра. {answer_count_motos(filter_list(update, context))}', reply_markup=InlineKeyboardMarkup(keyboard))
    context.user_data['list_motos_class'] = [i.cycle_class for i in (Motocycle.query.distinct(Motocycle.cycle_class).all())] #необходимо для генерации кнопок из списка существующих классов мотоциклов на момент запуска бота
    clear_filter #при повторном старте сбрасываем все фильтры



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
    SELECT_BRAND = set()
    SELECT_GEAR = set()
    SELECT_ENGINE_TYPE = set()
    SELECT_ENGINE_SIZE = set()
    SELECT_CLASS_MOTOCYCLE = set()
    context.user_data['selected_gear'] = SELECT_GEAR
    context.user_data['engine_size'] = SELECT_ENGINE_SIZE
    context.user_data['engine_type'] = SELECT_ENGINE_TYPE
    context.user_data['filter_by_brand'] = SELECT_BRAND
    context.user_data['selected_motocycle_class'] = SELECT_CLASS_MOTOCYCLE



def brands(update, context):
    keyboard = brands_nav(update, context)
    query = update.callback_query
    query.edit_message_text(f'Выберите один из брендов. {answer_count_motos(filter_list(update, context))}', reply_markup=InlineKeyboardMarkup(keyboard))


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
    return query.edit_message_text(f'Выберите один из брендов. {answer_count_motos(filter_list(update, context))}', reply_markup=InlineKeyboardMarkup(keyboard))


def button_filter(update, context):
    #function add to user_data brand name, motocycle class when you choose brand in filter
    query = update.callback_query
    selected_button = query['data'].split('|')
    if selected_button[0] == 'brand':
        if selected_button[1] in SELECT_BRAND:
            SELECT_BRAND.remove(selected_button[1])
        else:
            SELECT_BRAND.add(selected_button[1])
        context.user_data['filter_by_brand'] = SELECT_BRAND
        print(SELECT_BRAND)
    if selected_button[0] == 'class':
        if selected_button[1] in SELECT_CLASS_MOTOCYCLE:
            SELECT_CLASS_MOTOCYCLE.remove(selected_button[1])
        else:
            SELECT_CLASS_MOTOCYCLE.add(selected_button[1])
        context.user_data['selected_motocycle_class'] = SELECT_CLASS_MOTOCYCLE


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
    return query.edit_message_text(f'Выберите тип двигателя и объем. {answer_count_motos(filter_list(update, context))}', reply_markup=InlineKeyboardMarkup(keyboard))


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
    return query.edit_message_text(f' Выберите необходимый тип фильтра. {answer_count_motos(filter_list(update, context))}', reply_markup=InlineKeyboardMarkup(keyboard))


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
    query.edit_message_text(f'Выберите тип передачи. {answer_count_motos(filter_list(update, context))}', reply_markup=InlineKeyboardMarkup(keyboard))
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
    return query.edit_message_text(f'Выберите класс мотоцикла. {answer_count_motos(filter_list(update, context))}', reply_markup=InlineKeyboardMarkup(keyboard))


def filter_list(update, context):
    list_ids = []
    # возвращает обратно множество id мотоциклов для дальнейшей фильтрации

    filter_by_brand = set()
    filter_by_gear = set()
    filter_by_engine_type = set()
    filter_by_engine_size = set()
    filter_by_motocycle_class = set()

    try:
        dict_brands = requests.get(BASE_URL + '/brands').json()
        for brand in context.user_data['filter_by_brand']:
            brand_id = dict_brands[brand]
            for i in list(requests.get(BASE_URL + '/by_brand/' + str(brand_id)).json().keys()):filter_by_brand.add(i)
    except KeyError: pass

    try:
        for gear_type in context.user_data['selected_gear']:
            for i in list(requests.get(BASE_URL + '/by_gear_type/' + str(gear_type)).json().keys()):filter_by_gear.add(i)
    except KeyError: pass

    try:
        for engine in context.user_data['engine_type']:
            for i in list(requests.get(BASE_URL + '/engine_type/' + str(engine)).json().keys()):filter_by_engine_type.add(i)
    except KeyError: pass

    try:
        for engine in context.user_data['engine_size']:
            for i in list(requests.get(BASE_URL + '/engine/' + str(engine)).json().keys()):filter_by_engine_size.add(i)
    except KeyError: pass

    try:
        for motocycle_class in context.user_data['selected_motocycle_class']:
            for i in list(requests.get(BASE_URL + '/by_moto_class/' + str(motocycle_class)).json().keys()):filter_by_motocycle_class.add(i)
    except KeyError: pass

    filters = [filter_by_engine_type, filter_by_engine_size, filter_by_gear, filter_by_brand, filter_by_motocycle_class]
    for filter in filters:
        if len(list_ids) == 0:
            list_ids = filter
        elif len(filter) != 0:
            list_ids = list_ids.intersection(list(filter))
    return list_ids


def answer_count_motos(list_id):
    if len(list_id) == 0:
        return f'Найдено: {len(list_id)}'
    return f'Найдено: {len(list_id)}'


def take_motocycle_dict(id):
    motocycle_dict = requests.get(BASE_URL + '/by_id/' + str(id)).json()
    return motocycle_dict


def button_motocycle(motocycle_dict_properties):
    motocycle_name_button = f'{(motocycle_dict_properties["brands"])["brand_name"]} {motocycle_dict_properties["model"]} {motocycle_dict_properties["year_birth"]}'
    return motocycle_name_button


def listing_moto_list(update, context):
    query = update.callback_query
    query.answer()
    try:
        context.user_data['index_list_id']
    except KeyError:
        context.user_data['index_list_id'] = 0
    index_list_id = context.user_data['index_list_id']
    selected_button = query['data']
    if 'back_list_motocycle' in selected_button:
        index_list_id -= 4
        if index_list_id < 0:
            index_list_id = 0
    if 'next_list_motocycle' in selected_button:
        index_list_id += 4
        if index_list_id > len(filter_list(update, context)):
            index_list_id = len(filter_list(update, context)) - 4
    context.user_data['index_list_id'] = index_list_id


def show_list_motocycles(update, context):
    # show keyboard with founded motocycles
    list_id = list(filter_list(update, context))
    listing_moto_list(update, context)
    keyboard = []
    #if len(list_id) >= 4 and (context.user_data['index_list_id']+4 <= len(list_id)):
    if len(list_id) >= 4:
        try:
            for i in range(context.user_data['index_list_id'], context.user_data['index_list_id']+4):
                motocycle = take_motocycle_dict(list_id[i])
                keyboard.append([InlineKeyboardButton(button_motocycle(motocycle), callback_data=f'{list_id[i]}')])
        except KeyError: pass
    if len(list_id) < 4:
        for i in range(len(list_id)):
            motocycle = take_motocycle_dict(list_id[i])
            keyboard.append([InlineKeyboardButton(button_motocycle(motocycle), callback_data=f'{list_id[i]}')])
    query = update.callback_query
    back_to_menu = InlineKeyboardButton('меню', callback_data=str(back_menu))
    back_button = InlineKeyboardButton('<<назад', callback_data='back_list_motocycle')
    next_button = InlineKeyboardButton('вперед>>', callback_data='next_list_motocycle')
    keyboard.append([back_button, back_to_menu, next_button])
    return query.edit_message_text(f'Список найденных мотоциклов.', reply_markup=InlineKeyboardMarkup(keyboard))


def show_motocycle(update, context):
    message_cycle = OrderedDict()
    query = update.callback_query
    query.answer()
    motocycle_json = take_motocycle_dict(query['data'])
    message_cycle['Производитель'] = (motocycle_json.pop('brands'))['brand_name']
    message_cycle['Модель'] = motocycle_json.pop('model')
    message_cycle['Класс мотоцикл'] = motocycle_json.pop('cycle_class')
    message_cycle['Годы выпуска'] = motocycle_json.pop('year_birth')
    message_cycle['Объем двигателя'] = motocycle_json.pop('engine')
    message_cycle['Тип впрыска'] = motocycle_json.pop('type_engine')
    message_cycle['Количество цилиндров'] = motocycle_json.pop('cylinders')
    message_cycle['Тип передачи'] = motocycle_json.pop('gear_type')
    message_cycle['ABS'] = motocycle_json.pop('abs')
    message_cycle['Мощность'] = motocycle_json.pop('horse_power')
    message_cycle['Крутящий момент'] = motocycle_json.pop('torque')
    motocycle_string = str()
    for item in message_cycle:
        motocycle_string += (f'{item} : {message_cycle[item]} \n')
    update.callback_query.message.reply_text(f'{motocycle_string}')



