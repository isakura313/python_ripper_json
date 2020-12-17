# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import json
import re
import os
# https:\/\/cdn\d+\.ozone\.ru\/\w+\/\w+-\d+\/\w+\/\w+\.jpg
# \/context\/\w+\/\w+\/\d+\/\?\w+\=\w+

def str_fix(price):
    price = str(price).split()
    price.reverse()
    price.pop(0)
    price.reverse()
    return int(''.join(price))


headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
range_of_pages = int(input("Сколько страниц вы хотите обработать? \n"))
URL = input('Введите URL раздела Ozon, который вас интересует \n')
whole_data = []
count = 0
for j in range(1, range_of_pages):
    if j == 1:
        # URL = 'https://www.ozon.ru/brand/apple-26303000/category/smartfony-15502/'
        path_now = os.getcwd()
        page = requests.get(URL, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        results1 = soup.find_all('img', srcset = re.compile('https:\/\/cdn\d+\.ozone\.ru\/\w+\/[a-z-\-\d+]+\/\w+\/\w+\.jpg')) # получаем изображение
        results2 = soup.find_all('span', {"class": "b5v6"})  # получение ценника b5v4
        price_size = soup.find_all('div', {"class": "b5v4"}) # получение ценника b5v4
        results2_5 = soup.find_all('span', {"class": "b5v9"}) # получение старого ценника
        results3 = soup.find_all('a', {"class": "a2g0"}) # название товара
        results4 = soup.find_all('div', {"class": "a1y6"}) # рейтинг товара
        for i in range(0, len(results1)):
            data = {}
            print(f'Объект номер {count}')
            data['id'] = count
            print(results1[i]['src'])
            data['img'] = results1[i]['src']
            print(results2[i].text)
            data['price'] = str_fix(results2[i].text)
            if len(price_size[i]) == 2:
                print(True)
                data['discount'] = True
                # print(price_size[i].find('span', {"class": "b5v9"}).text)
                # data['new_price'] = price_size[i].find('span', {"class": "b5v9"}).text
                new_price = price_size[i].find('span', {"class": "b5v9"}).text
                data['old_price'] = str_fix(new_price)
            elif len(price_size[i]) == 1:
                print(False)
                data['discount'] = False
            print(results3[i].text)
            data['title'] = results3[i].text
            print(results4[i]['title'])
            data['rating'] = results4[i]['title']
            whole_data.append(data)
            count = count + 1
    else:
        payload = {'page': j}
        print(whole_data)
        # URL = f'https://www.ozon.ru/highlight/28039/'
        page = requests.get(URL, headers=headers, params = payload)
        soup = BeautifulSoup(page.content, 'html.parser')
        # print(soup)
        results1 = soup.find_all('img', srcset = re.compile('https:\/\/cdn\d+\.ozone\.ru\/\w+\/[a-z-\-\d+]+\/\w+\/\w+\.jpg')) # получаем изображение
        results2 = soup.find_all('span', {"class": "b5v6"})  # получение ценника b5v4
        price_size = soup.find_all('div', {"class": "b5v4"}) # получение ценника b5v4
        results2_5 = soup.find_all('span', {"class": "b5v9"}) # получение старого ценника
        results3 = soup.find_all('a', {"class": "a2g0"}) # название товара
        results4 = soup.find_all('div', {"class": "a1y6"}) # рейтинг товара
        for i in range(0, len(results1)):
            data = {}
            print(f'Объект номер {count}')
            data['id'] = count
            print(results1[i]['src'])
            data['img'] = results1[i]['src']
            print(results2[i].text)
            data['price'] = str_fix(results2[i].text)
        
            if len(price_size[i]) == 2:
                print(True)
                data['discount'] = True
                # print(price_size[i].find('span', {"class": "b5v9"}).text)
                # data['new_price'] = price_size[i].find('span', {"class": "b5v9"}).text
                new_price = price_size[i].find('span', {"class": "b5v9"}).text
                data['old_price'] = str_fix(new_price)
            elif len(price_size[i]) == 1:
                print(False)
                data['discount'] = False
            print(results3[i].text)
            data['title'] = results3[i].text
            print(results4[i]['title'])
            data['rating'] = results4[i]['title']
            whole_data.append(data)
            count = count + 1
print(whole_data)
with open('product.json', 'w+', encoding="utf-8") as outfile:
    # whole_data.encode("UTF-8")
    json.dump(whole_data, outfile, ensure_ascii=False)
    # outfile.write(whole_data)