#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import sys
from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
import requests
import json
import movieanalysis

def default_function():
    #douban TOP 250
    print('Scraping top 250 movie data from douban website and saving as movie_info_Top250.csv')
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36"}
    def movie_urls(n):
        movie_urls = []  #250 urls 
        for i in range(0,n,25):
            url = 'https://movie.douban.com/top250?start={}&filter='.format(i)
            req = requests.get(url, headers=headers)  
            soup = BeautifulSoup(req.text, 'html.parser')
            items = soup.find('ol', class_='grid_view').find_all('li')
            for item in items:
                movie_href = item.find('div', class_='hd').find('a')['href']
                movie_urls.append(movie_href)
            time.sleep(1)
        return movie_urls
    def get_movie_info(url):
        req = requests.get(url, headers=headers)
        soup = BeautifulSoup(req.text, 'html.parser')
        item = soup.find('div', id='content')
        movie = {}
        movie['电影名称'] = item.h1.span.text
        movie_info = item.find('div', id='info').text.replace(' ', '').split('\n')  
        for i in movie_info:
            if ':' in i:
                movie[i.split(':')[0]] = i.split(':')[1]
            else:
                continue
        movie['评分'] = item.find('div', id='interest_sectl').find('div', class_='rating_self clearfix').find('strong', class_='ll rating_num').text
        movie['评分人数'] = item.find('div', id='interest_sectl').find('div', class_='rating_self clearfix').find('div', class_='rating_sum').find('span', property='v:votes').text
        return movie
    def main_func():
        movies = movie_urls(250) #list of 250 urls
        print('Collected number of movie urls', len(movies))
        movie_info = []   #list of dics
        error_href = []
        for url in movies:
            try:
                movie_info.append(get_movie_info(url)) 
                print('url:', url, 'scraped successfully.')
            except:
                error_href.append(url)
                print('url:', url, 'ERROR.')
            time.sleep(2)    
        print('Done!')
        print('Collected number of movie data', len(movie_info))
        print('Error href', len(error_href))    
        return (movie_info, error_href)
    result = main_func()
    df = pd.DataFrame(result[0]) 
    #df.drop(['官方网站','官方小站'], axis=1, inplace=True)
    #df.to_csv('movie_info_Top250.csv', index=False)   
    print('The dimension of the dataset:', df.shape)
    print('Samples:')
    print(df.head())
    print('Existing error href:')
    print(result[1])
    print('Why we get errors here is that douban website has locked our account because of the frequent access.')
    
    #IMDB TOP 250
    print('Acquiring top 250 movie data from IMDB using IMDB API and saving as imdb_movie_info.csv')
    url = 'https://imdb-api.com/en/API/Top250Movies/k_w7cj8b1c'
    payload = {}
    headers= {}
    response = requests.request("GET", url, headers=headers, data = payload)
    dic = json.loads(response.text)
    df = pd.DataFrame(dic['items'])
    #df.to_csv('imdb_movie_info.csv', index=False)
    print('The dimension of the dataset:', df.shape)
    print('Samples:')
    print(df.head())
    
    #douban box office
    print('Scraping douban movies box office data from "box office mojo".')
    df = pd.read_csv('movie_info_Top250.csv')
    douban_movie_id = list(df['IMDb'])
    domestic_boxoffice = []
    international_boxoffice = []
    worldwide_boxoffice = []
    for id in douban_movie_id:
        url = f'https://www.boxofficemojo.com/title/{id}/?ref_=bo_se_r_1'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        items = soup.find('div', id='a-page').find_all('div', class_='a-section a-spacing-none')
        try:
            domes = items[1].find('span', class_='money').text
            domestic_boxoffice.append(domes)
        except:
            domestic_boxoffice.append('None')
        try:
            inter = items[2].find('span', class_='money').text
            international_boxoffice.append(inter)
        except:
            international_boxoffice.append('None')
        try:
            world = items[3].find('span', class_='money').text
            worldwide_boxoffice.append(world)
        except:
            worldwide_boxoffice.append('None')
        time.sleep(1)
    print(len(domestic_boxoffice), 'box office data successfully acquired.')
    dic = {}
    dic['domestic_boxoffice'] = domestic_boxoffice
    dic['international_boxoffice'] = international_boxoffice
    dic['worldwide_boxoffice'] = worldwide_boxoffice
    dff = pd.DataFrame(dic)
    print('The dimension of the dataset:', dff.shape)
    print('Samples:')
    print(dff.head())
    
    #IMDB BOX OFFICE
    print('Scraping IMDB movies box office data from "box office mojo", merging into IMDB dataset, and saving as imdb_top250_with_boxoffice.csv')
    df = pd.read_csv('imdb_movie_info.csv')
    imdb_movie_id = list(df['id'])
    domestic_boxoffice = []
    international_boxoffice = []
    worldwide_boxoffice = []
    for id in imdb_movie_id:
        url = f'https://www.boxofficemojo.com/title/{id}/?ref_=bo_se_r_1'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        items = soup.find('div', id='a-page').find_all('div', class_='a-section a-spacing-none')
        try:
            domes = items[1].find('span', class_='money').text
            domestic_boxoffice.append(domes)
        except:
            domestic_boxoffice.append('None')
        try:
            inter = items[2].find('span', class_='money').text
            international_boxoffice.append(inter)
        except:
            international_boxoffice.append('None')
        try:
            world = items[3].find('span', class_='money').text
            worldwide_boxoffice.append(world)
        except:
            worldwide_boxoffice.append('None')
        time.sleep(1)
    print(len(domestic_boxoffice), 'box office data successfully acquired.')
    dic = {}
    dic['domestic_boxoffice'] = domestic_boxoffice
    dic['international_boxoffice'] = international_boxoffice
    dic['worldwide_boxoffice'] = worldwide_boxoffice
    dff = pd.DataFrame(dic)
    print('The dimension of the dataset:', dff.shape)
    print('Samples:')
    print(dff.head())

    movieanalysis.show_analysis()

def static_function():
    movieanalysis.show_analysis()

if __name__ == '__main__': #for your purpose, you can think of this line as the saying "run this chunk of code first"
    if len(sys.argv) == 1: # this is basically if you don't pass any additional arguments to the command line
        #default mode
        #print eveything or the dimensions and a sample 
        default_function()
        
    elif sys.argv[1] == '--static': # if you pass '--static' to the command line
        #static mode
        static_function()

