import requests
import lxml
from bs4 import BeautifulSoup

url = "https://www.rottentomatoes.com/top/bestofrt/"

f = requests.get(url)
soup = BeautifulSoup(f.content, 'lxml')                         # create object BeautifulSoup specify parser
movies = soup.find('table', {'class': 'table'}).find_all('a')   # <table class="table">
movies_lst = []
num = 0

for anchor in movies:
                                                               # # # # # # # # # # # # # # # # # # # # # #
    urls = 'https://www.rottentomatoes.com' + anchor['href']    # info needed to take a movie description #
    movies_lst.append(urls)                                     # ex. <a href="/m/it_happened_one_night"  #
    num += 1                                                    # # # # # # # # # # # # # # # # # # # # # #
    movie_url = urls
    movie_f = requests.get(movie_url)
    movie_soup = BeautifulSoup(movie_f.content, 'lxml')
    movie_content = movie_soup.find('div', {'class': 'movie_synopsis clamp clamp-6 js-clamp'})
    print(num, urls, '\n', 'Movie:' + anchor.string.strip())
    print('Movie info:' + movie_content.string.strip())
