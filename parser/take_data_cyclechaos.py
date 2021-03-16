from bs4 import BeautifulSoup
import os
from api import model
from lxml import html
from db_settings import db_session



def motorcycle_properties(file_name):
    page = open(file_name).read()
    tree = html.fromstring(page)
    properties = tree.xpath("/html/body/div[3]/div[3]/div[4]/div/table[1]/tbody")
    return properties


def motorcycle_properties_BF4(file_name):
    print(file_name)
    bike_name = False
    page = open(file_name).read()
    soup = BeautifulSoup(page, 'lxml')
    prop = soup.find('table', class_='infobox h-product hproduct motorcycle').find('tbody') #сотрем .find_all('tr')
    try:
        bike_name = html.fromstring(page).xpath("/html/body/div[3]/div[3]/div[4]/div/table[1]/tbody/tr[2]/td/b/text()")[
            0]
    except IndexError:
        pass

    """В цикле пробегаем по строчкам и достаем текст, условие позволяет вытащить только те свойства, 
    которые полные и имеют название. Имя мотоцикла вытаскивается отдельно."""
    if bike_name:
        brand_name, model, list_properties = collecting_rows_properties(prop, bike_name)
        return brand_name, model, list_properties


def take_other_pages(file):
    bike_name = False
    # функция вытаскивает данные, т.к. на некоторых страницах названия таблиц и разметка отличаются
    page = open(file).read()
    soup = BeautifulSoup(page, 'lxml')
    prop = soup.find('table', class_='infobox h-product hproduct motorcycle').find('tbody')
    bike_name = soup.find('td', class_='fn p-name').get_text()

    if bike_name:
        brand_name, model, list_properties = collecting_rows_properties(prop, bike_name)
        return brand_name, model, list_properties


def write_data_to_db(brand_name, model, list_properties):
    #сюда мы должны передать бренд, модель + ТТХ, функция возвращает "класс" мотоцикл, в котором ТТХ
    motocycle = model.Motocycle(brand_name, model)
    for i in list_properties:
        if i[0] == 'Production':
            motocycle.year_birth = i[1]
        if i[0] == 'Engine':
            try:
                volume = int(''.join(filter(str.isdigit, i[1])))
                if volume < 8001:
                    motocycle.engine = volume
            except ValueError:
                continue
        if i[0] == 'Horsepower':
            motocycle.horse_power = i[1]
        if i[0] == 'Final Drive' or 'Final Drive' in i[1]:
            if 'chain' in i[1].lower():
                motocycle.gear_type = 'chain'
            elif 'belt' in i[1].lower():
                motocycle.gear_type = 'belt'
            elif 'shaft' in i[1].lower():
                motocycle.gear_type = 'shaft'
        if 'carburetor' in i[1]:
            motocycle.type_engine = 'carburetor'
        if 'injection' in i[1]:
            motocycle.type_engine = 'injection'
        if 'Class' in i[0]:
            motocycle.cycle_class = i[1]
    db_session.add(motocycle)
    db_session.commit()


def collecting_rows_properties(prop, bike_name):
    brand_name = False
    list_properties = []
    for row in prop.find_all('tr'):
        x = [row.get_text(strip=True) for row in row.find_all('th')]
        y = [row.get_text(strip=True) for row in row.find_all('td')]
        if len(x) != 0 and len(y) != 0 and len(x[0]) > 0 and len(y[0]) > 0:
            properties_scraped = [x[0], y[0]]
            list_properties.append(properties_scraped)
            if x[0] == 'Manufacturer':
                brand_name = y[0]
                model = bike_name.replace(str(brand_name), "").strip()
    if brand_name and model:
        return brand_name, model, list_properties


if __name__ == '__main__':
    list_files = os.listdir('pages_cyclechaos')
    os.chdir('pages_cyclechaos')
    for file in list_files:
        unable_to_parse_as_chart = True
        try:
            brand_name, model, list_properties = motorcycle_properties_BF4(file)
            if brand_name and model and list_properties:
                unable_to_parse_as_chart = False
            else:
                brand_name, model, list_properties = take_other_pages(file)
            write_data_to_db(brand_name, model, list_properties)
        except TypeError:
            pass
        except UnicodeDecodeError:
            pass
        except AttributeError:
            pass