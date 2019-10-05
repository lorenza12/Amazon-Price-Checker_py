import requests
import urllib.request
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

import sys
sys.path.append('../')
import Modules.Helper_Functions as Helper_Functions


def request_html(url ,header_counter=1, timeout_time=15):
    """Returns html from a given url

       Param: url to get html, header_counter for a specefic request header (optional), timeout_time on how ong the request timeout has (optional)
    """
    request_header = get_header(header_counter)

    try:
        response = requests.get(url, headers=request_header, timeout=timeout_time)

        if (response.status_code == 200):
                #amazon.com is loaded mianly by javascript and by using the BeautifulSoup method twice allows you to build the html
                soup = BeautifulSoup(response.content, 'html.parser')
                soup_html = BeautifulSoup(soup.prettify(), "html.parser")

                return soup_html

        else:
            return None

    except Exception as e:
        #Log error
        
        message = f'request_html error {str(e)} \n paramaters: url - {url}  header_counter - {header_counter} timeout_time - {timeout_time}'
        Helper_Functions.write_log(message,0)

        return None

def get_header(counter=1):
    """Returns a browser header for web scraping

       Param: (optional) counter to return a certain header

       Amazon does a weird thing where a header will work one time, then not the next so making fucntion hold them all
       to be able to cycle through them until we find one that works
    """
    user_agent = UserAgent()
    
    switcher = {
        1:user_agent.ie,
        2:user_agent.msie,
        3:user_agent['Internet Explorer'],
        4:user_agent.opera,
        5:user_agent.chrome,
        6:user_agent.google,
        7:user_agent['google chrome'],
        8:user_agent.firefox,
        9:user_agent.ff,
        10:user_agent.safari,
    }

    try:
        header = {'User-Agent': str(switcher[counter])}
    except Exception as e:
        #return a working header
        
        message = f'get_header error {str(e)} \n paramaters: counter - {counter}'
        Helper_Functions.write_log(message,0)
        
        header = {'User-Agent': str(user_agent.chrome)}

    return header
    

def get_title(html):
    #get the title of the item
    try:
        title = html.find(id= "productTitle").text
        return title.strip()
    except:
        return None

def get_price(html):
    #get the price of the item
    try:
        price = html.find(id= "priceblock_ourprice").text
        return price.strip()
    except:
        return None

def get_deal_price(html):
    #sometimes items are on sale and their actual price is listed here
    try:
        deal_price = html.find(id= "priceblock_dealprice").text
        return deal_price.strip()
    except:
        return None




if __name__ == "__main__":
    #testing - run this file directly to check if working
    
    url = 'https://www.amazon.com/Official-Python-Logo-Developers-T-Shirt/dp/B07QR5K7VZ/ref=sr_1_65?keywords=python&qid=1564959822&s=gateway&sr=8-65'
 
    response_html = request_html(url)

    title = get_title(response_html)
    price = get_price(response_html)
    sale = get_deal_price(response_html)

    print('title: ' + (title if title != None else '-'))
    print('price: ' + (price if price != None else '-'))
    print('sale price: ' + (sale if sale != None else '-'))
    
