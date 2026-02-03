import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

from bs4.element import AttributeValueList
base_url='https://books.toscrape.com/catalogue/page-{}.html'
headers={'user-agent':"Mozilla/5.0"}
book_data={}
book_name1=[]
book_price=[]
title=[]
page=1

while True:
  url=base_url.format(page)
  response=requests.get(url,headers=headers)
  if response.status_code!=200:
    break
  soup=BeautifulSoup(response.text,'lxml')
  books=soup.find_all('article',class_='product_pod')
  if not books:
    break
  for book in books:

    #fetching book names
    #book_name1.append(book.find('h3').find('a').get('title'))
    
    title.append(book.h3.a["title"])
    book_data['Title']=title
  #checking the price
    price=book.find('p',class_='price_color').text
    book_price.append(price)
    book_data['Price']=book_price

  #checking the availaibility
    Availability=book.find('p',class_='instock availability').text.strip()
    book_data['Availability']=Availability
  
  #fetching rating details
    rating=book.p['class'][1]
    book_data['Rating']=rating


    #fetching 
  page+=1
  time.sleep(1)
df = pd.DataFrame(book_data, columns=[
    "Title", "Price", "Rating", "Availability"])

df.to_csv("books_data.csv", index=False)

print("\n✅ Data saved to books_data.csv")

