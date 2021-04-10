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
    keyboard.append(search_keyboard())
    keyboard.append([back_button, search, next_button])
    keyboard.append([InlineKeyboardButton('поиск по всем', callback_data=str('all'))])
    return keyboard

def start_bot(update, context):
    keyboard = []
    update.message.reply_text('Привет. Я wiki бот по мотоциклам. \n'
                              'Ты можешь посмотреть краткую справочную информацию по моделям мотоциклов. \n'
                              )
    keyboard_brands = brands_nav()
    update.message.reply_text(f'Выберите один из брендов', reply_markup=InlineKeyboardMarkup(keyboard_brands))
    return SEARCH


def search_keyboard(brand_index=None, next=False, back=False):
    row = []
    keyboard = []
    dict_brands = requests.get(BASE_URL + '/brands').json()
    brands_list = list(dict_brands.keys())
    if brand_index == None:
        for brand_index in range(3):
            row.append(InlineKeyboardButton(brands_list[brand_index], callback_data=str(brands_list[brand_index])))
        return row
    elif (brand_index + 3) <= len(brands_list) and next == True:
        for i in range(brands_list, brands_list + 3):
            row.append(InlineKeyboardButton(brands_list[i], callback_data=str(brands_list[i])))
        return keyboard.append(row)
    elif (brand_index + 3) > len(brands_list) and next == True:
        ####тут просто можно написать генератор, вероятно и в других случаях, генератор списка кнопок
        for i in range(brand_index, len(brands_list)):
            row.append(InlineKeyboardButton(brands_list[i], callback_data=str(brands_list[i])))
        return keyboard.append(row)
    elif (brand_index - 3) >= 0 and back == True:
        x = brand_index - 3
        for i in range(x, brands_list):
            row.append(InlineKeyboardButton(brands_list[i], callback_data=str(brands_list[i])))
        return keyboard.append(row)
    elif (brand_index - 3) < 0 and back == True:
        for i in range(brand_index):
            row.append(InlineKeyboardButton(brands_list[i], callback_data=str(brands_list[i])))
        return keyboard.append(row)


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