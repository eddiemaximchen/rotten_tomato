from bs4 import BeautifulSoup
from urllib.request import urlopen
import json

url='https://www.rottentomatoes.com/m/facing_the_laughter_minnie_pearl'
html = urlopen(url)
bs = BeautifulSoup(html.read(),'html.parser')
data=bs.find_all('h1')
movie=[]
title=data[0].get_text()
movie.append({
    'title':title
})

data=bs.find('p',{'class':'scoreboard__info'}).get_text()
movie.append({
    'year':data[0],
    'type':data[1]
})

#AUDIENCE SCORE
data=bs.find('div',{'class':'thumbnail-scoreboard-wrap'}).findChildren()
movie.append({
    'audiencescore':data[4].attrs['audiencescore']
})
#storyline
data=bs.find('div',{'id':'movieSynopsis'}).get_text()
movie.append({
    'story':data.strip('\n').strip()
})
#stars
stars=bs.find_all('div',{'class':'cast-item'})
for star in stars:
    starName=star.get_text().strip()
    if 'Unknown' in starName:
        continue
    else:
        movie.append({
            'star':starName[:20].strip()
        }) 
#save as json
with open(f"Theater/{title}.json", "w", encoding="utf-8") as file:
    file.write(json.dumps(movie, ensure_ascii=False, indent=4))