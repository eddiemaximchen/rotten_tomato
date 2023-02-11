from bs4 import BeautifulSoup
from urllib.request import urlopen
import json
import os
import pandas as pd
url='https://www.rottentomatoes.com/m/congratulations_2023'
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
length=len(data1)
for i in range(length):
    content_str=content_str+'*'+data1[i].strip()
if length==1:
    content_str=content_str+'*'
#AUDIENCE SCORE
data=bs.find('score-board')
content_str=content_str+'*'+data.attrs['audiencescore']
if data.attrs['audiencescore']=="":
    content_str=content_str+'*'
#storyline
story=bs.find('div',{'id':'movieSynopsis'}).get_text().strip('\n')
if story=='':
    content_str=content_str+'*'+'N/A'
else:
    content_str=content_str+'*'+story.strip()
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
movie1=[]
if length==1:
    movie1.append({
        'name':movie[0],
        'year':movie[1],
        'type':'',
        'howlong':movie[2],
        'score':movie[3],
        'story':movie[4],
        'stars':movie[5]
        })
else:
     movie1.append({
        'name':movie[0],
        'year':movie[1],
        'type':movie[2],
        'howlong':movie[3],
        'score':movie[4],
        'story':movie[5],
        'stars':movie[6]
    })
#save as json
with open(f"Theater/{title}.json", "w", encoding="utf-8") as file:
    file.write(json.dumps(movie1, ensure_ascii=False, indent=4))
