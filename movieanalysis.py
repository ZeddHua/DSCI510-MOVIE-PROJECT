#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#import libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
from wordcloud import WordCloud

def show_analysis():
    df = pd.read_csv('douban_top250_with_boxoffice.csv')

    print('douban movie type analysis')

    #movie types count
    lst1 = list(df['类型'])
    lst2 = [i.split('/') for i in lst1]
    movie_types = [j for i in lst2 for j in i]
    movie_types_set = list(set(movie_types))
    type_count = []
    for i in movie_types_set:
        count = movie_types.count(i)
        type_count.append(count)

    #type_count_df
    dic = {"movie_type": movie_types_set, "type_count": type_count}
    type_df = pd.DataFrame(dic)
    type_df.sort_values("type_count", ascending=False, inplace=True)

    #translation
    english_type_dic = {"剧情":'Drama', "爱情":'Romance', "喜剧":'Comedy', "冒险":'Adventure', "犯罪":'Crime', "奇幻":'Fantasy', "动画":'Animation', "惊悚":'Thriller', "动作":'Action', "悬疑":'Mystery', "科幻":'Science-Fiction', "家庭":'Family', "战争":'War', "传记":'biographical', "古装":'Costume', "音乐":'Music', "历史":'Historical', "同性":'LGBTQ+', "歌舞":'Musical', "儿童":'Children', "武侠":'Martial Arts', "纪录片":'Documentary', "西部":'Westerns', "灾难":'Disaster', "情色":'Adult', "恐怖":'Horror', "运动":'Sports'}
    type_df['movie_type'] = type_df['movie_type'].map(english_type_dic)

    #visualization
    x = type_df['movie_type']
    y = type_df['type_count']
    plt.figure(figsize=(20,6))
    plt.title('TOP 250 movie types count')
    plt.xticks(rotation=45)
    plt.bar(x,y)
    plt.show()

    #wordcloud
    plt.figure()
    s = ' '.join(list(type_df['movie_type']))
    wc = WordCloud(background_color='white', width=3000, height=2000).generate(s)
    #get_ipython().run_line_magic('pylab', 'auto')
    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")

    print('''Douban movie type analysis.
    This analysis is mainly focused on the types of Top 250 movies in douban websites. 
    We can see what types top movies prefer to. 
    Through the bar chart, we can notice that drama movie is the most poular movie type in douban top 250 movies 
    and romance, comedy, adventure and other kinds of movies are less popular. 
    In order to see this trend much more clearly, a wordcloud diagram is created, 
    which shows most popular movie types in large font size and less popular types in smaller size.''')

    print('douban movie country/region analysis')

    #country count
    lst1 = list(df['制片国家/地区'])
    lst2 = [i.split('/') for i in lst1]
    country = [j for i in lst2 for j in i]
    country_set = list(set(country))
    country_count = []
    for i in country_set:
        count = country.count(i)
        country_count.append(count)

    #country_count_df
    dic = {"country": country_set, "country_count": country_count}
    country_df = pd.DataFrame(dic)
    country_df.sort_values("country_count", ascending=False, inplace=True)

    #translation
    #english_country_dic = {"剧情":'Drama', "爱情":'Romance', "喜剧":'Comedy', "冒险":'Adventure', "犯罪":'Crime', "奇幻":'Fantasy', "动画":'Animation', "惊悚":'Thriller', "动作":'Action', "悬疑":'Mystery', "科幻":'Science-Fiction', "家庭":'Family', "战争":'War', "传记":'biographical', "古装":'Costume', "音乐":'Music', "历史":'Historical', "同性":'LGBTQ+', "歌舞":'Musical', "儿童":'Children', "武侠":'Martial Arts', "纪录片":'Documentary', "西部":'Westerns', "灾难":'Disaster', "情色":'Adult', "恐怖":'Horror', "运动":'Sports'}
    #country_df['country'] = country_df['country'].map(english_country_dic)

    #visualization
    x = country_df['country']
    y = country_df['country_count']
    plt.figure(figsize=(20,6))
    plt.rcParams['font.sans-serif'] = ['SimHei'] 
    plt.rcParams['axes.unicode_minus'] = False 
    plt.title('TOP 250 movie country count')
    plt.xticks(rotation=45)
    plt.bar(x,y)
    plt.show()

    #pie chart
    x = country_df['country']
    y = country_df['country_count']
    lst = list(np.zeros(len(country_set), dtype=np.int))
    lst[0] = 0.1
    explode = lst
    plt.figure(figsize=(6,6))
    plt.pie(y, labels = x, explode = explode, startangle = 90, counterclock = False, autopct="%.f%%", pctdistance=0.7, shadow=True)
    plt.title('TOP 250 movie country count pie chart')
    plt.axis('square')
    plt.show()

    print('''Country/region analysis. 
    In this analysis, I create a bar chart and a pie chart to see the country/region trend of movies. 
    Results present to us that in douban top 250 movie list, American movie occupies a quite large proportion. 
    What next to it are movies made from Japan, England, Hongkong, China mainland.''')

    print('combine analysis')

    df1 = pd.read_csv('douban_top250_with_boxoffice.csv')
    df2 = pd.read_csv('imdb_top250_with_boxoffice.csv')

    print('shared movies analysis')

    set1 = set(df1.IMDb)
    set2 = set(df2.id)
    shared_id = list(set1 & set2)
    print('Length of shared movies:', len(shared_id))

    print('''Shared movies analysis.
    I scraped the top 250 movies data separately from douban website and IMDB website. 
    Douban website is a famous movie website in China, and IMDB is the international movie database. 
    The topic I want to analyze most is how different are those movies on the lists. 
    Through above tentative analysis, we find out that in those top 250 movie lists, 95 movies are overlapped. 
    Let's find out more information about these movies.  ''')

    df_shared_movies = df1.query('IMDb in @shared_id')

    #movie types count
    lst1 = list(df_shared_movies['类型'])
    lst2 = [i.split('/') for i in lst1]
    movie_types = [j for i in lst2 for j in i]
    movie_types_set = list(set(movie_types))
    type_count = []
    for i in movie_types_set:
        count = movie_types.count(i)
        type_count.append(count)

    #type_count_df
    dic = {"movie_type": movie_types_set, "type_count": type_count}
    type_df = pd.DataFrame(dic)
    type_df.sort_values("type_count", ascending=False, inplace=True)

    #translation
    english_type_dic = {"剧情":'Drama', "爱情":'Romance', "喜剧":'Comedy', "冒险":'Adventure', "犯罪":'Crime', "奇幻":'Fantasy', "动画":'Animation', "惊悚":'Thriller', "动作":'Action', "悬疑":'Mystery', "科幻":'Science-Fiction', "家庭":'Family', "战争":'War', "传记":'biographical', "古装":'Costume', "音乐":'Music', "历史":'Historical', "同性":'LGBTQ+', "歌舞":'Musical', "儿童":'Children', "武侠":'Martial Arts', "纪录片":'Documentary', "西部":'Westerns', "灾难":'Disaster', "情色":'Adult', "恐怖":'Horror', "运动":'Sports'}
    type_df['movie_type'] = type_df['movie_type'].map(english_type_dic)

    #wordcloud
    plt.figure()
    s = ' '.join(list(type_df['movie_type']))
    wc = WordCloud(background_color='white', width=3000, height=2000).generate(s)
    #get_ipython().run_line_magic('pylab', 'auto')
    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")

    #country count
    lst1 = list(df_shared_movies['制片国家/地区'])
    lst2 = [i.split('/') for i in lst1]
    country = [j for i in lst2 for j in i]
    country_set = list(set(country))
    country_count = []
    for i in country_set:
        count = country.count(i)
        country_count.append(count)

    #country_count_df
    dic = {"country": country_set, "country_count": country_count}
    country_df = pd.DataFrame(dic)
    country_df.sort_values("country_count", ascending=False, inplace=True)

    #pie chart
    x = country_df['country']
    y = country_df['country_count']
    lst = list(np.zeros(len(country_set), dtype=np.int))
    lst[0] = 0.1
    explode = lst
    plt.figure(figsize=(6,6))
    plt.pie(y, labels = x, explode = explode, startangle = 90, counterclock = False, autopct="%.f%%", pctdistance=0.7, shadow=True)
    plt.title('TOP 250 movie country count pie chart')
    plt.axis('square')
    plt.show()

    print('''We can see that movies belong to both top lists are mostly drama, crime genre as the word cloud diagram shows. 
    Also, most of them come from American and England as the pie chart shows.''')

    print('movie rating analysis')

    #rating comparision
    df1_rating_describe = pd.DataFrame(df1['评分'].describe())
    df2_rating_describe = pd.DataFrame(df2.imDbRating.describe())
    dff = pd.concat([df1_rating_describe, df2_rating_describe], axis=1)
    dff.rename(columns={"评分":'doubanRating'}, inplace=True)
    print(dff)

    sns.distplot(df1['评分'], hist=False, kde_kws={"color":"red","linestyle":"-"}, norm_hist=True, label="douban")
    sns.distplot(df2['imDbRating'], hist=False, kde_kws={"color":"blue","linestyle":"--"}, norm_hist=True, label="imdb")
    plt.title("Top 250 movies rating")
    plt.legend()
    plt.show()

    print('''Comparision in movie rating. 
    We are able to see that the ratings in douban website are between 8.3 and 9.7 while those in IMDB are between 8.0 and 9.2. 
    The rating mean is higher in douban movie rating. With the help of the visualization, 
    we can see the distribution of the ratings in two datasets. The rating distribution in imdb dataset is more to the left.''')

    print('worldwide box office analysis')

    df1 = pd.read_csv('douban_top250_with_boxoffice.csv')
    df2 = pd.read_csv('imdb_top250_with_boxoffice.csv')

    #delete none box office movies
    df1.drop(df1[df1['worldwide_boxoffice']=='None'].index, inplace=True)
    df1['worldwide_boxoffice'] = df1['worldwide_boxoffice'].apply(lambda x: int(x.replace('$','').replace(',','')))
    df2.drop(df2[df2['worldwide_boxoffice']=='None'].index, inplace=True)
    df2['worldwide_boxoffice'] = df2['worldwide_boxoffice'].apply(lambda x: int(x.replace('$','').replace(',','')))

    #sort df by box office
    df1_sort = df1.sort_values("worldwide_boxoffice", ascending=False)
    df2_sort = df2.sort_values("worldwide_boxoffice", ascending=False)

    #create df for vis
    df1_boxoffice_top10 = df1_sort[['电影名称','worldwide_boxoffice']].head(10).reset_index()
    df1_boxoffice_top10.drop(['index'], axis=1, inplace=True)
    df2_boxoffice_top10 = df2_sort[['title','worldwide_boxoffice']].head(10).reset_index()
    df2_boxoffice_top10.drop(['index'], axis=1, inplace=True)
    df_boxoffice_top10 = pd.concat([df1_boxoffice_top10, df2_boxoffice_top10], axis=1)
    print(df_boxoffice_top10)

    #df1_sort visualization
    x = df1_sort.head(10)['电影名称']
    y = df1_sort.head(10)['worldwide_boxoffice']
    plt.figure(figsize=(13,6))
    plt.rcParams['font.sans-serif'] = ['SimHei'] 
    plt.rcParams['axes.unicode_minus'] = False 
    plt.title('douban Top 10 box office movies')
    plt.barh(x,y)
    plt.show()

    #df2_sort visualization
    x = df2_sort.head(10)['title']
    y = df2_sort.head(10)['worldwide_boxoffice']
    plt.figure(figsize=(13,6))
    plt.title('IMDB Top 10 box office movies')
    plt.barh(x,y)
    plt.show()

    print('''Worldwide box office analysis. 
    In this analysis, I grabbed top 10 movies with highest worldwide box office in both datasets. 
    It turns out that the ranks of movies in the top 250 lists have little to do with the box office. 
    Few of those movies in top 10 box office lists belong to the top 10 movies lists in general.''')

