import requests as req
from bs4 import BeautifulSoup as Soup
import time

cit_url = 'https://scholar.google.com/scholar.bib?q=info:PapID:scholar.google.com/&output=cite'
St = time.time()
r = Soup(req.get('https://scholar.google.com/scholar?q=query+expansion+using+word').text, 'html.parser')
for result in r.find_all(class_='gs_rt'):
    id = result.find('a')['id']
    cit = cit_url.replace('PapID', id)
    cit_r = Soup(req.get(cit).text, 'html.parser')
    bibtex = cit_r.find('a')['href']
    print(req.get(bibtex).text)

print(time.time() - St)