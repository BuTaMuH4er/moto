import logging, requests, uuid, time
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed


logging.basicConfig(filename='bike_wiki_pars.log', level=logging.ERROR,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')

headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:85.0) Gecko/20100101 Firefox/85.0'}

def take_urls(url):
    links = set()
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, 'lxml')
    urls = soup.findAll('span', class_='mw-headline')
    #достаем ссылки по разделам с техникой(мото, мопеды и т.д.)
    for link in urls:
        if link.b.a != None:
            href = url+link.b.a['href']   #ссылки на разделы мотоциклы, мопеды и т.п.   ТУТ только 3 ссылки
            links.add(href)
    return links

def page_urls(url):
    #возвращает список ссылок на конкретные модели со всей страницы
    main_url = 'http://www.bikerwiki.ru'
    bikes_pages = dict()
    #собираем огромный список на модели мотоциклов
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, 'lxml')
            #собираем все ссылки на странице по каждой модели
            #не хватает перелистывания на следующу страницу
    for bikes_url in (soup.select("div.mw-category-group a[href]")):
        bikes_pages[bikes_url['title']] = main_url + bikes_url['href']
    return bikes_pages


def next_page(url):
    main_url = 'http://www.bikerwiki.ru'
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, 'lxml')
    asd = soup.find('a', text='Следующая страница')
    try:
        return (main_url + asd['href'])
    except TypeError:
        return False


def download_file(url, file_name):
    try:
        html = requests.get(url, stream=True)
        with open(f'pages_biker_wiki/{file_name}.html', 'wb') as data_file:
            data_file.write(html.content)
        return html.status_code
    except requests.exceptions.RequestException as e:
        return logging.error(f'Request error while saving data {e}')


def runner(url_list):
    threads = []
    count = 0
    good_result = 0
    with ThreadPoolExecutor(max_workers=10) as executor:
        for url in url_list:
            file_name = uuid.uuid1()
            threads.append(executor.submit(download_file, url, file_name))
            count += 1
            if (count % 1000) == 0:
                time.sleep(300)
        for task in as_completed(threads):
            print(task.result())
            if task.result() == 200:
                good_result += 1
    print(good_result)


if __name__ == '__main__':
    logging.info('Parse start')
    links_count = 0
    url = 'http://www.bikerwiki.ru'
    main_urls = take_urls(url)
    pages_links = set()
    link_links = []
    for link in main_urls:
        pages_links.add(link)
        while link:
            link = next_page(link)
            if link == True:
                pages_links.add(link)
    all_moto_links = set()
    for link in pages_links:
        pack_links = page_urls(link).values()
        for i in pack_links:
            link_links.append(i)
    runner(link_links)
    print(links_count)
