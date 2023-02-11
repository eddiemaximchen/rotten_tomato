from bs4 import BeautifulSoup
from urllib.request import urlopen
import json

url='https://www.rottentomatoes.com/m/facing_the_laughter_minnie_pearl'
html = urlopen(url)
bs = BeautifulSoup(html.read(),'html.parser')
data=bs.find_all('h1')
movie=[]
content_str=''
title=data[0].get_text()
content_str=content_str+title

#year and movie type
data=bs.find('p',{'class':'scoreboard__info'}).get_text()
data1=data.split(',')
content_str=content_str+'*'+data1[0]+'*'+data1[1].strip()

#AUDIENCE SCORE
data=bs.find('div',{'class':'thumbnail-scoreboard-wrap'}).findChildren()
content_str=content_str+'*'+data[4].attrs['audiencescore']
#storyline
data=bs.find('div',{'id':'movieSynopsis'}).get_text().strip('\n')
content_str=content_str+'*'+data.strip()
# stars
stars=bs.find_all('div',{'class':'cast-item'})
content_str=content_str+'*'
for star in stars:
    starName=star.get_text().strip()
    if 'Unknown' in starName:
        continue
    else:
        content_str=content_str+' '+starName[:20].strip()
movie=content_str.split('*')
#save as json
with open(f"Theater/{title}.json", "w", encoding="utf-8") as file:
    file.write(json.dumps(movie, ensure_ascii=False, indent=4))
