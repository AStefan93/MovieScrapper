import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

imdb_url_page1 = "https://www.imdb.com/search/title/?groups=top_100&sort=user_rating,desc&view=simple"
imdb_url_page2 = "https://www.imdb.com/search/title/?groups=top_100&view=simple&sort=user_rating,desc&start=51&ref_=adv_nxt"
rotten_tomatoes_url = "https://www.rottentomatoes.com/top/bestofrt/"
metacritic_url = "https://www.metacritic.com/browse/movies/score/metascore/all/filtered?view=condensed"

headers = {"Accept-Language": "en-US, en;q=0.5"}

imdb1_results = requests.get(imdb_url_page1, headers)
imdb2_results = requests.get(imdb_url_page2, headers)
rotten_tomatoes_results = requests.get(rotten_tomatoes_url, headers)
metacritic_results = requests.get(metacritic_url, headers={'User-Agent': 'Mozilla/5.0'})

imdb_soup1 = BeautifulSoup(imdb1_results.text, "html.parser")
imdb_soup2 = BeautifulSoup(imdb2_results.text, "html.parser")
rotten_tomatoes_soup = BeautifulSoup(rotten_tomatoes_results.text, "html.parser")
metacritic_soup = BeautifulSoup(metacritic_results.text, "html.parser")

#imdb_movie_div1 = imdb_soup1.find_all('div', class_='lister-item mode-simple')
imdb_movie_div1 = imdb_soup1.find_all('div', class_='col-title')
#imdb_movie_div2 = imdb_soup2.find_all('div', class_='lister-item mode-simple')
imdb_movie_div2 = imdb_soup2.find_all('div', class_='col-title')
rotten_tomatoes_movie_div = rotten_tomatoes_soup.find_all('table', class_='table')
metacritic_movie_div = metacritic_soup.find_all('table', class_='clamp-list condensed')

imdb_titles1 = []
imdb_titles2 = []
rotten_tomatoes_titles = []
metacritic_titles = []

for container in imdb_movie_div1:
    name = container.a.text
    imdb_titles1.append(name)
for container in imdb_movie_div2:
    name = container.a.text
    imdb_titles2.append(name)
for container in rotten_tomatoes_movie_div:
    a_names = container.findAll('a', class_='unstyled articleLink')
    for a in a_names:
        name = a.text
        name = name.lstrip()
        rotten_tomatoes_titles.append(name)
for container in metacritic_movie_div:
    tds = container.findAll('td', class_='details')
    for td in tds:
        name = td.a.h3.text
        metacritic_titles.append(name)

imdb_titles = imdb_titles1 + imdb_titles2

titles = []
for meta_movie in metacritic_titles:
    for rotten_movie in rotten_tomatoes_titles:
        for imdb_movie in imdb_titles:
            if meta_movie in rotten_movie or meta_movie in imdb_movie or rotten_movie in imdb_movie:
                titles.append(meta_movie)

titles = list(dict.fromkeys(titles))

title_file = open('titles2.txt','w')
for title in titles:
    print(title, file=title_file)
title_file.close()