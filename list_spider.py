 # --codeing=utf-8--
from bs4 import BeautifulSoup
import re
import requests
import urllib.request
import urllib.error
import xlwt
import sqlite3

"""
提取当前steam热销榜首页所有独立游戏的价格、链接、评价、发行日期，并生成excel表格
价格过滤基于人民币计算，需要使用中国大陆IP访问


"""

# 如果使用正则表达式
# findLink = re.compile(r'<a href="(.*?)">')
# findImgSrc = re.compile(r'<img.*src="(.*?)"', re.S)
# findTitle = re.compile(r'<span class="title">(.*?)</span>')
# findReview = re.compile(r'search_review_summary(.*?)"')
# findReleased=re.compile(r'<div class="col search_released responsive_secondrow">(.*?)</div>')
# findPrice=re.compile(r'<div class="col search_price discounted responsive_secondrow">(.*?)</div>')


def main():
    baseurl = "https://store.steampowered.com/search/?tags=492&filter=topsellers"
    # askURL(baseurl)
    datalist = getData(baseurl)
    savepath = r'./SteamTopSellers.xls'
    saveData(datalist, savepath)

# 进行url请求


def askURL(url):
    head = {
        "User-Agent": "Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 80.0.3987.122  Safari / 537.36"
    }
    html = ""
    try:
        r = requests.get(url, headers=head)
        html = r.text
        print('get request success')
    # 抛出异常
    except requests.exceptions.ConnectionError:
        print('ConnectionError occured! please try again')
    except requests.exceptions.HTTPError as e:
        print('HTTPError occured! error info:', e, ' please try again')
    except:
        print('unkown error occured,please try again')
    return html

# 获取数据


def getData(baseurl):
    datalist = []
    html = askURL(baseurl)
    # print(html)
    soup = BeautifulSoup(html, "html.parser")
    # print(soup)
    for game in soup.find_all('div', class_='responsive_search_name_combined'):
        data = []
        # 查找标题
        title = game.span
        data.append(title.text)
        # 查找发行日期
        released = game.find(
            'div', class_='col search_released responsive_secondrow')
        data.append(released.text)
        # 查找好评率
        reviewInfo = game.find(
            'div', class_='col search_reviewscore responsive_secondrow')
        #print(reviewInfo.span)
        if(reviewInfo.span != None):
            review = reviewInfo.span['data-tooltip-html']
            data.append(re.findall('(.*?)<br>', review)[0])
        else:
            data.append('None')
        # 查找价格,并判断是有折扣
        price = game.find(
            'div', class_='col search_price_discount_combined responsive_secondrow')
        # print(price)
        if(price.find('div', class_='col search_price responsive_secondrow') != None):
            origin = price.find(
                'div', class_='col search_price responsive_secondrow')
            #print(origin)
            data.append(re.findall(r'\¥ \d+', origin.text)
                        [0])  # 正则表达式过滤掉价格以外的内容
            data.append(re.findall(r'\¥ \d+', origin.text)[0])
        else:
            discounted = game.find(
                'div', class_='col search_price discounted responsive_secondrow')
            orign = discounted.strike
            data.append(orign.text)
            data.append(re.findall(r'\¥ \d+', discounted.text)
                        [1])  # 正则表达式过滤掉价格以外的内容
        # 查找游戏steam链接
        link = game.parent['href']
        # print(link)
        data.append(link)
        datalist.append(data)
    return datalist


# 保存文件
def saveData(datalist, savepath):
    print("saving-----------")
    book = xlwt.Workbook(encoding="utf-8", style_compression=0)
    sheet = book.add_sheet('topsellers', cell_overwrite_ok=True)
    col = ("name", "released_date", "review",
           "origin_price", "discounted_price", "link")
    for i in range(0, 6):
        sheet.write(0, i, col[i])
    for i in range(0, len(datalist)):
        data = datalist[i]
        for j in range(0, len(data)):
            sheet.write(i+1, j, data[j])
    book.save(savepath)


if __name__ == "__main__":
    main()
    print('resolved')
