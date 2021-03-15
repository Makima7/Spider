# --codeing=utf-8--
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

"""
    将表格中每个游戏名做好处理，在目录创建其对应文件夹，并记录信息
    根据表格内容抓取图片并保存


"""


def main():
    tasklist = []
    newAddPath()
    tasklist = createtask()
    saveImg(tasklist)

# 根据games目录中记录的信息生成指向社区截图的链接 并生成链接+游戏目录名的列表


def createtask():
    tasklist = []
    pathlist = os.listdir(r'./games')
    for path in pathlist:
        try:
            with open(r'./games/'+path+r'/info.txt') as f:
                infoURL = f.read()
        except OSError as e:
            print('错误信息：'+e+path+'链接信息可能不存在，请检查')
            continue

        # 根据链接判断该url指向一个游戏还是dlc
        if(re.findall(r'app/.*?/', infoURL) != []):
            id = re.findall(r'app/(.*?)/', infoURL)[0]
            imgURL = r'https://steamcommunity.com/app/'+id+r'/screenshots/?p=1&browsefilter=mostrecent'
            # 生成一条带url和图片保存位置的task
            task = []
            task.append(imgURL)
            task.append(path)
        else:
            shutil.rmtree(r'./games/'+path)
            print(path+'非游戏本体,已经在目录中删除')

        tasklist.append(task)
    # print(tasklist)
    return tasklist

    return 0

# 根据表格信息收集需要爬取图片的游戏名称，统一去除特殊字符后为游戏在目录下建立一个文件夹用于存放图片，并生成一个文本文档记录该游戏的steam商店链接


def newAddPath():
    pathlist = []
    book = xlrd.open_workbook('SteamTopSellers.xls')
    sheet = book.sheets()[0]
    gamelist = sheet.col_values(0)[1:]
    print("本次新增游戏目录：")
    for i in range(0, len(gamelist)):
        rootpath = './games'
        try:
            # 创建目录
            path = os.path.join(rootpath, re.sub('\W+', '', gamelist[i]))
            os.makedirs(path)
            pathlist.append(path)
            with open(path+r'/info.txt', 'w') as info:
                # 创建信息文件，用于记录游戏商店url
                info.write(sheet.cell(i+1, 5).value)
            print(gamelist[i])
        except FileExistsError as e:
            continue
    print("目录变更完成\n -------------------------------------")
    return pathlist


# 根据任务列表中的url和保存路径，下载图片并保存下来


def saveImg(tasklist):
    for task in tasklist:
        url = task[0]
        path = task[1]
        print("开始下载 "+path+"图片"+url)
        r = askURL(url)
        html = r.text
        soup = BeautifulSoup(html, "html.parser")
        imgs = soup.find_all('img', class_="apphub_CardContentPreviewImage")
        # 统计现有图片
        num = len(os.listdir('./games/'+path))-1
        for img in imgs:
            #print(img['src'])
            r = askURL(img['src'])
            downloadpath = './games/'+path+'/img'+str(num)+'.jpg'
            with open(downloadpath, 'wb') as f:
                f.write(r.content)
                time.sleep(3)
            num = num+1
        time.sleep(3)

    print("所有任务执行完毕，请检查")


def askURL(url):
    head = {
        "User-Agent": "Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 80.0.3987.122  Safari / 537.36"
    }
    # steam社区有墙，需要使用代理
    proxy = {
        "http": "socks5://127.0.0.1:10808",
        "https": "socks5://127.0.0.1:10808"
    }

    html = ""
    try:
        r = requests.get(url, headers=head, proxies=proxy)
        print('get request success')
    # 抛出异常
    except requests.exceptions.ConnectionError:
        print('ConnectionError occured! please try again')
    except requests.exceptions.HTTPError as e:
        print('HTTPError occured! error info:', e, ' please try again')
    except:
        print('unkown error occured,please try again')
    return r


if __name__ == "__main__":
    main()
    print('resolved')
