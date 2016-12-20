import urllib2
import bs4
from bs4 import BeautifulSoup

url="https://www.google.com/partners/#a_search;qury=apple"
html=urllib2.urlopen(url)
soup=BeautifulSoup(html)
a=soup.find('title')
print a