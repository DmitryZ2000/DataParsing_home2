import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from pprint import pprint
import json

url = 'https://books.toscrape.com'
ua = UserAgent()
headers = {"User-Agent": ua.random}
# params = {"page": 1}
session = requests.session()

all_books = []
page_number = 1

while True:
    response = session.get(url + "/catalogue/page-" + str(page_number) + '.html',  headers=headers)
    soup = BeautifulSoup(response.content, features="html.parser")
    books = soup.find_all(name='article', attrs={'class': 'product_pod'})

    for book in books:
        book_info = {}
        
        book_info_name = book.find('a')
        book_info['name'] = book_info_name.find('img')['alt']
        book_info['url'] = url+ '/catalogue/' + book_info_name['href']
        book_info['price'] = float(book.find('div', {'class': 'product_price'}).
                                find('p', {'class': 'price_color'}).getText()[1:])
        book_info['rating'] = str(book.find_all('p', {'class': "star-rating"})). \
                                split('\n')[0].split(' ')[-1][:-2]
        all_books.append(book_info)

    print(f'Обработано страница {page_number}')
# Альтернатива выхода из цикла while    
    # try: 
    #     next_page = soup.find('li', {'class': 'next'}).getText()
    #     page_number += 1
    # except:
    #     break
# -----------------------------------
    next_page = soup.find('li', {'class': 'next'})
    if not next_page:
        break
    page_number += 1

# pprint(all_books, sort_dicts=False)
print(f'Всего имеем {len(all_books)} публикаций')

# dic_2_json = json.dumps(all_books, indent=2)
# print(dic_2_json)

with open('books.json', 'w', encoding='utf-8') as f:
    json.dump(all_books, f, ensure_ascii=False)