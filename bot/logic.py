from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
import requests

BASE_URL = 'http://localhost:5000'

SEARCH = range(1)

def start_bot(update, context):
    update.message.reply_text('Приивет. Я wiki бот по мотоциклам. \n'
                              'Ты можешь посмотреть краткую справочную информацию по моделям мотоциклов. \n'
                              'тили-тили-трали-вали, тут еще мы не писали')
    return SEARCH


def search_keyboard(update, context):
    dict_brands = requests.get(BASE_URL+'/brands').json()
    brands = dict_brands.keys()
    keyboard = ReplyKeyboardMarkup([brands])
    #keyboard = ReplyKeyboardMarkup([['/button']])
    update.message.reply_text(f'Клава-клава', reply_markup=keyboard)

def search_by(brand=None, birth_year=None, model=None, engine=None):
    url_brands = BASE_URL+'/by_brand/'+ brand
    #url_by_id = BASE_URL+'/'+str(67)
    result = requests.get(url_brands)
    print(result.json())


def stop(update, context):
    update.message.reply_text(f'Досвидания')
    return ConversationHandler.END


if __name__ == '__main__':
    search_keyboard()
#TODO: загрузить бренды в user_context и предложить их выбрать.
#перечисление через , или пробле, использовать регулярку для получения списка мотоциклов
