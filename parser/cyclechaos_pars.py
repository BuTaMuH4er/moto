from bs4 import BeautifulSoup
from lxml import html
import requests, uuid, time
from concurrent.futures import ThreadPoolExecutor, as_completed


def get_list_brands(url):
    list_links = []
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:85.0) Gecko/20100101 Firefox/85.0'}
    page = requests.get(url, headers=headers).text
    tree = html.fromstring(page)
    # Берем с главной страницы список брендов и ссылки на них
    links = tree.xpath("//div[@id = 'p-Brands']/div[@class = 'body']/ul//li/a/@href")
    # в цикле по каждому бренду вытаскиваем все возможные ссылки на модели
    for i in range(len(links)):
        links[i] = url + links[i]
        tree = html.fromstring(requests.get(links[i], headers=headers).text)
        list_moto_links = tree.xpath('//div[@class = "mw-parser-output"]/ul/li/a/@href')
        for j in range(len(list_moto_links)):
            list_links.append(url + list_moto_links[j])
    return list_links


def download_file(url, file_name):
    try:
        html = requests.get(url, stream=True)
        open(f'pages_cyclechaos/{file_name}.html', 'wb').write(html.content)
        return html.status_code
    except requests.exceptions.RequestException as e:
        return e


def runner(url_list):
    threads = []
    count = 0
    good_result = 0
    with ThreadPoolExecutor(max_workers=8) as executor:
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


def write_list_links(name_file, data):
    with open(name_file, 'w') as file:
        file.write(data+'\n')

if __name__ == '__main__':
    cyclechaos = 'https://www.cyclechaos.com'
    all_motocycles = get_list_brands(cyclechaos) #all need links
    print(len(all_motocycles))
    runner(all_motocycles)