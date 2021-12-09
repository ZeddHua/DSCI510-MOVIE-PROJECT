Libraries needed:
import sys
from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
import requests
import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
from wordcloud import WordCloud

How to run my codes:
pip install -r requirements.txt
e.g. python movie_project.py
e.g. python movie_project.py --static 

Notices:
1. Douban movie website need to login to obtain information. And occasions occur when you scrape the data, the account locks because of frequent access. There won't be errors popping up, but you will see the error hrefs collected in a list. Also, I set 'time.sleep(2)' to avoid account locking issue, so the programme may be quite slow.
2. In the project, I need box office data for both douban and IMDB movies. So I scraped the box office data two times. Once for douban movies box office and another time for IMDB movies box office.
3. Four datasets obtaining processes are written in the .py file. The next scraper can run only when the former one has finished. So it may be slow.  
