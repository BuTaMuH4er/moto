from bs4 import BeautifulSoup
import os
from lxml import html

def motorcycle_properties(file_name):
    page = open(file_name).read()
    tree = html.fromstring(page)
    properties = tree.xpath("/html/body/div[3]/div[3]/div[4]/div/table[1]/tbody")
    return properties


def motorcycle_properties_BF4(file_name):
    list_properties = []
    page = open(file_name).read()
    soup = BeautifulSoup(page, 'lxml')
    prop = soup.find('table', class_ = 'infobox h-product hproduct motorcycle').find('tbody').find_all('tr')
    try:
        bike_name = html.fromstring(page).xpath("/html/body/div[3]/div[3]/div[4]/div/table[1]/tbody/tr[2]/td/b/text()")[0]
    except IndexError:
        pass
    #print(bike_name)

    """В цикле пробегаем по строчкам и достаем текст, условие позволяет вытащить только те свойства, 
    которые полные и имеют название. Имя мотоцикла вытаскивается отдельно."""

    for row in prop:
        x = [row.get_text(strip=True) for row in row.find_all('th')]
        #print(x)
        y = [row.get_text(strip=True) for row in row.find_all('td')]
        #print(y)
        if len(x) != 0 and len(y) != 0 and len(x[0]) > 0 and len(y[0]) > 0:
            properties_scraped = [x[0],y[0]]
            list_properties.append(properties_scraped)
    return list_properties, str(bike_name)


if __name__ == '__main__':
    list_files = os.listdir('pages_cyclechaos')
    os.chdir('pages_cyclechaos')
    count_attrer = 0
    count_unbonder = 0
    for file in list_files:
        try:
            out_file = motorcycle_properties_BF4(file)
        except UnicodeDecodeError:
            pass
        except AttributeError:
            count_attrer += 1
            pass
        except UnboundLocalError:
            file = '9cc09f0e-7a15-11eb-9904-38f9d328d19b.json'
            page = open(file).read()
            soup = BeautifulSoup(page, 'lxml')
            x = soup.find('table', class_ = 'infobox h-product hproduct motorcycle')
            if x:
                count_unbonder += 1
            #break
            pass
    print(count_attrer, 'attr error')
    print(count_unbonder, 'unbound error')
        #motorcycle_properties(file)
    #with open('pages_cyclechaos')

