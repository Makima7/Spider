from bs4 import BeautifulSoup
import os
import re
import requests
import urllib.request
import urllib.error
import xlrd
import pandas
import shutil
import time


def main():
    url = "https://steamcommunity.com/app/1145360/screenshots/"
    html = askurl(url)
    soup = BeautifulSoup(html, "html.parser")
    imgs = soup.find_all('img', class_="apphub_CardContentPreviewImage")
    for img in imgs:
        print(img['src'])
    #print(html)


def askurl(url):
    head = {
        "User-Agent": "Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 80.0.3987.122  Safari / 537.36", 
        # cookie":""
    }
    proxy = {
        "http": "socks5://127.0.0.1:10808",
        "https": "socks5://127.0.0.1:10808"
    }
   
    html = ""
    try:
        r = requests.get(url,headers=head,proxies=proxy)
        html = r.text
        print('get request success')
    # 抛出异常
    except requests.exceptions.ConnectionError as e:
        print('ConnectionError occured! please try again')
    except requests.exceptions.HTTPError as e:
        print('HTTPError occured! error info:', e, ' please try again')
    except:
        print('unkown error occured,please try again')
    return html


if __name__ == "__main__":
    main()
    print('resolved')
