from bs4 import BeautifulSoup
from urllib.request import urlopen
import json

html = urlopen(url)
bs = BeautifulSoup(html.read(),'html.parser')
movies=bs.find_all('a',{'class':'js-tile-link'})
links=[]
for a in movies:
    if a.has_attr('href'):
        title=a['href'][3:]
        links.append({
            'title':title,
            'path':'https://www.rottentomatoes.com'+a['href']
        })
# 寫入 書籍資訊 in json 檔
with open('movies_athome.json', "w", encoding="utf-8") as file:
    file.write(json.dumps(links, ensure_ascii=False, indent=4))
