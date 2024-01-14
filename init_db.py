from bs4 import BeautifulSoup
from pymongo import MongoClient
import requests,certifi

client = MongoClient('mongodb+srv://sparta:jungle@cluster0.jxnelzd.mongodb.net/?retryWrites=true&w=majority',tlsCAFile=certifi.where())
db = client.books

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
url = 'https://www.yes24.com/Product/Category/BestSeller?categoryNumber=001&pageNumber=1&pageSize=50'

data = requests.get(url,headers=headers)
soup = BeautifulSoup(data.text,'html.parser')
books = soup.select('#yesBestList > li')
db.book.drop()

i = 1
for book in books:
    title = book.select_one('a.gd_name').text.strip()
    img_url = book.select_one('em.img_bdr > img')['data-original']
    auth = book.select_one('span.info_auth > a').text
    href = book.select_one('a.gd_name')['href']
    href = 'https://yes24.com' + href
    db.book.insert_one({'no': str(i),"title" : title, "img_url" : img_url, "auth" : auth, "href" : href, "like" : 0})
    i+=1
print("init finished")

