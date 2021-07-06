import requests
from bs4 import BeautifulSoup as BS
import concurrent.futures
import pandas as pd

raw_url = "http://books.toscrape.com"

class Scraper():

    def __init__(self,raw_url, number_of_pages):
        self._url = raw_url
        self._number_of_pages = number_of_pages
        self.books = []
        # self.proxy = "69.30.242.214:2000"   ## Not to get blocked by the website or not to get RE-Captcha every request - Proxy is the way to go.  robots.txt mostly is the reason


    def __str__(self):
        return (f"Scraper for {self._url} with {self._number_of_pages} number of pages")

    def __repr__(self):
        return (f"{self._url}, {self._number_of_pages} pages")

    def total_number_of_pages(self): #Getting iterable value of pages in total
        return list(x for x in range(1,self._number_of_pages+1))

    def find_ingredients(self,number_of_page):
        self._url = requests.get(f"{raw_url}/catalogue/page-{number_of_page}.html")#, proxies={"http": self.proxy, "https": self.proxy})        #sends url.request and saves as a value
        self.soup = BS(self._url.text,'html.parser') #parses it as a readable text
        for i in self.soup.find_all('li', class_="col-xs-6 col-sm-4 col-md-3 col-lg-3"): #looks for the data in the class 'col-xs-6 col-sm-4 col-md-3 col-lg-3'
            ipi = requests.get('http://httpbin.org/ip').text.split()[2]
            title = i.find('h3').getText()
            price = i.find('p',class_= "price_color").getText()
            for k,v in i.find('p', class_="star-rating").attrs.items():
                star_rating = v[1]
            almost = str(i.find('div',class_="image_container").find("a")).split("src=")[-1]# 1st part of the img link
            link = ("http://books.toscrape.com"+almost.split('"')[1][2:]) #complete img link
            in_stock = str(i.find("p",class_="instock availability").getText()).split()[0]+" "+str(i.find("p",class_="instock availability").getText()).split()[1]
            self.books.append({
                "title" : title,
                "price" : price,
                "star_rating" : star_rating,
                "link" : link,
                "in_stock" : in_stock,
                "IP" : ipi,
            })# gathers books' data as vocabularies and stores into list


    def cook_soup(self): # Multithreading, making the whole process alot faster########   Gathers info of each book on every page.
        with concurrent.futures.ThreadPoolExecutor() as exector:
            exector.map(self.find_ingredients, self.total_number_of_pages())


    def pour_soup(self): # Splits gathered data into parts and prepares for PANDAS' output as Excel file
        titles = []
        prices = []
        stars = []
        urls = []
        in_stocks = []
        IPs = []

        for book in self.books:
            titles.append(book["title"])
            prices.append(book["price"])
            stars.append(book["star_rating"])
            urls.append(book["link"])
            in_stocks.append(book["in_stock"])
            IPs.append(book["IP"])

        data = {"Title": titles,
                "Prices": prices,
                "Stars": stars,
                "Links": urls,
                "Stock": in_stocks,
                "IP":IPs
                }

        df = pd.DataFrame(data=data)
        df.index += 1
        df.to_excel("C:\\testing\\output.xlsx")

    def serve_soup(self):
        self.cook_soup()
        self.pour_soup()



scrape = Scraper(raw_url,50)


scrape.serve_soup()
#Each website is unique, doing this script OOP makes no reasonable sense, but practice is practice :)