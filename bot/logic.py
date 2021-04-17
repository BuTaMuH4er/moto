from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
import requests

BASE_URL = 'http://localhost:5000'
#Stages
SEARCH = range(1)
# Callback data
next, back, searching = range(3)

def brands_nav(update, context):
    keyboard = []
    try:
        brand_index = context.user_data['brand_index']
        print(f'{brand_index} в самом начала брендс нав')
    except KeyError:
        context.user_data['brand_index'] = None
        brand_index = context.user_data['brand_index']
    #buttons for 2nd row buttons
    back_button = InlineKeyboardButton('<<назад', callback_data=str(back))
    search = InlineKeyboardButton('поиск', callback_data=str(searching))
    next_button = InlineKeyboardButton('вперед>>', callback_data=str(next))
    keyboard.append(search_keyboard(update,context))
    keyboard.append([back_button, search, next_button])
    keyboard.append([InlineKeyboardButton('поиск по всем', callback_data=str('all'))])
    print(f'brands_nav конец функции функции {brand_index}')
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

#тут первый принт!
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
        for i in range(brand_index, brand_index + 3):
            row.append(InlineKeyboardButton(brands_list[i], callback_data=str(brands_list[i])))
            #context.user_data['brand_index'] = brand_index + 3
        keyboard.append(row)
        return row
        #return keyboard
    elif brand_index > len(brands_list):
        for i in range(brand_index, len(brands_list)):
            row.append(InlineKeyboardButton(brands_list[i], callback_data=str(brands_list[i])))
        return keyboard.append(row)
    #back
    elif brand_index < 0:
        for i in range(brand_index):
            row.append(InlineKeyboardButton(brands_list[i], callback_data=str(brands_list[i])))
        return keyboard.append(row)


"""def next_brand(update, context):
    print(f'кто-то запросил следующие бренды')
    query = update.callback_query
    query.answer()
    index = context.user_data['brand_index']
    context.user_data['brand_index'] = index + 3
    query.edit_message_text(text='Добавить бренд в фильтр')
    return SEARCH"""

def next_brand(update, context):
    print(f'Старт кнопки next')
    query = update.callback_query
    query.answer()
    index = context.user_data['brand_index']
    context.user_data['brand_index'] = index + 3
    keyboard = brands_nav(update, context)
    print(f'попытка обновить клавиатуру')
    new_keyboard(update, context, keyboard)

#из функций переключения по списку мы передаем бренд_индекс через юзер_дата, дальше сравниваем какое значение
#у бренд индекса и исходя из этого передаем значения в серч_кейбор и делаем кнопки

def back_brand(update, context):
    query = update.callback_query
    query.answer()
    index = context.user_data['brand_index']
    context.user_data['brand_index'] = index - 3
    return SEARCH


def searching(update, context):
    print(f'Нажали на кнопку поиска')
    #query = update.callback_query
    #query.answer()
    #update.message.reply_text(f'Поиск нажат')

def stop(update, context):
    update.message.reply_text(f'Досвидания')
    return ConversationHandler.END


def new_keyboard(update, context, keyboard):
    query = update.callback_query
    print(len(keyboard), '\n', keyboard)
    return query.edit_message_text(f'Выберите один из брендов', reply_markup=InlineKeyboardMarkup(keyboard))
    #return update.message.edit_message_text(f'Выберите один из брендов', reply_markup=InlineKeyboardMarkup(keyboard))


#if __name__ == '__main__':
#   search_keyboard()