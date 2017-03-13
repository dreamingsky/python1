import urllib.request
from bs4 import BeautifulSoup
try:
    page = urllib.request.urlopen("http://www.dytt8.net/html/gndy/dyzz/20170310/53447.html").read()
    soup = BeautifulSoup(page,"lxml")
    print(soup.find_all(True))
except Exception as e:
    print(e)
