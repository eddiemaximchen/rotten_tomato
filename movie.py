import json
# 操作 browser 的 驅動程式
from selenium import webdriver
# 負責開啟和關閉 Chrome 的套件
from selenium.webdriver.chrome.service import Service
# 自動下載 Chrome Driver 的套件
from webdriver_manager.chrome import ChromeDriverManager
# 例外處理的工具
from selenium.common.exceptions import TimeoutException
# 面對動態網頁，等待、了解某個元素的狀態，通常與 exptected_conditions 和 By 搭配
from selenium.webdriver.support.ui import WebDriverWait
# 搭配 WebDriverWait 使用，對元素狀態的一種期待條件，若條件發生，則等待結束，往下一行執行
from selenium.webdriver.support import expected_conditions as EC
# 期待元素出現要透過什麼方式指定，經常與 EC、WebDriverWait 一起使用
from selenium.webdriver.common.by import By
# 取得系統時間的工具
from datetime import datetime
# 強制停止/強制等待 (程式執行期間休息一下)
from time import sleep
# 處理下拉式選單的工具
from selenium.webdriver.support.ui import Select
# 隨機取得 User-Agent
from fake_useragent import UserAgent
ua = UserAgent()
# 啟動瀏覽器工具的選項
my_options = webdriver.ChromeOptions()
# my_options.add_argument("--headless")                # 不開啟實體瀏覽器背景執行
my_options.add_argument("--start-maximized")         # 最大化視窗
my_options.add_argument("--incognito")               # 開啟無痕模式
my_options.add_argument("--disable-popup-blocking")  # 禁用彈出攔截
my_options.add_argument("--disable-notifications")   # 取消通知
my_options.add_argument(f'--user-agent={ua.random}') # (Optional)加入 User-Agent
driver = webdriver.Chrome(options = my_options,service = Service(ChromeDriverManager().install()))
import pandas as pd
#in theaters
path_list=pd.read_json('movies_athome_150.json')
links=[]
for path in path_list['path']:
    url = path
    driver.get(url)
    # 強制等待
    sleep(2)
    #假裝人點進去直到圖片出現
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "img.posterImage")))            
    movie_pic=driver.find_element(By.CSS_SELECTOR,"img.posterImage").get_attribute('src')
    path=driver.current_url
    title=path[33:]
    yeartypetime=driver.find_element(By.CSS_SELECTOR,"p.scoreboard__info").text
    yeartypetime1=yeartypetime.split(',')
    lengtgh=len(yeartypetime1)
    if(lengtgh==3):
        year=yeartypetime1[0]
        type=yeartypetime1[1]
        howlong=yeartypetime1[2]
    if(lengtgh==2):
        year=yeartypetime1[0]
        type=yeartypetime1[1]
        howlong=''
    if(lengtgh==1):
        year=yeartypetime1[0]
        type=''
        howlong=''
    score=driver.find_element(By.TAG_NAME,"score-board").get_attribute('audiencescore')
    story=driver.find_element(By.CSS_SELECTOR,"div#movieSynopsis").text.strip("\n")
    stars=driver.find_elements(By.CSS_SELECTOR,"div.cast-item")
    starlist=[]
    for star in stars:
        starlist.append(star.text)
    starlist1=" ".join(starlist)
    links.append({
        'title':title,
        'path':path,
        'year':year,
        'type':type,
        'howlong':howlong,
        'score':score,
        'story':story,
        'stars':starlist1,
        'pic':movie_pic
        
    })
driver.close()
# 寫入 書籍資訊 in json 檔
with open('movies_athome_150.json', "w", encoding="utf-8") as file:
    file.write(json.dumps(links, ensure_ascii=False, indent=4))
