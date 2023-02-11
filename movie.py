from bs4 import BeautifulSoup
from urllib.request import urlopen
import json
import os

'''
匯入套件
'''

# 操作 browser 的 API
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
# 處理逾時例外的工具
from selenium.common.exceptions import TimeoutException
# 面對動態網頁，等待某個元素出現的工具，通常與 exptected_conditions 搭配
from selenium.webdriver.support.ui import WebDriverWait
# 搭配 WebDriverWait 使用，對元素狀態的一種期待條件，若條件發生，則等待結束，往下一行執行
from selenium.webdriver.support import expected_conditions as EC
# 期待元素出現要透過什麼方式指定，通常與 EC、WebDriverWait 一起使用
from selenium.webdriver.common.by import By
# 強制等待 (執行期間休息一下)
from time import sleep
# 子處理程序，用來取代 os.system 的功能
import subprocess

# 啟動瀏覽器工具的選項
my_options = webdriver.ChromeOptions()
# my_options.add_argument("--headless")                #不開啟實體瀏覽器背景執行
my_options.add_argument("--start-maximized")         #最大化視窗
my_options.add_argument("--incognito")               #開啟無痕模式
my_options.add_argument("--disable-popup-blocking") #禁用彈出攔截
my_options.add_argument("--disable-notifications")  #取消 chrome 推播通知

# 使用 Chrome 的 WebDriver
driver = webdriver.Chrome(options = my_options,service = Service(ChromeDriverManager().install()))


#Most popular 網址最多到第五頁 滑動捲軸按more可以有更多頁
#in theaters
#https://www.rottentomatoes.com/browse/movies_in_theaters/?page=5
#at home
#https://www.rottentomatoes.com/browse/movies_at_home/?page=5
#tv shows
#https://www.rottentomatoes.com/browse/tv_series_browse/?page=5
#all time list-->還沒抓
#https://editorial.rottentomatoes.com/all-time-lists/ 

#in theaters
url = 'https://www.rottentomatoes.com/browse/tv_series_browse/?page=5'

#先用seleinum把more按到底再開始抓 學習捲動
html = urlopen(url)
bs = BeautifulSoup(html.read(),'html.parser')
movies=bs.find_all('a',{'class':'js-tile-link'})
links=[]
for a in movies:
    if a.has_attr('href'):
        title=a['href'][3:]
        links.append({
            'title':title,
            'path':'https://www.rottentomatoes.com/'+a['href']
        })
# 寫入 書籍資訊 in json 檔
with open('movies_athome.json', "w", encoding="utf-8") as file:
    file.write(json.dumps(links, ensure_ascii=False, indent=4))