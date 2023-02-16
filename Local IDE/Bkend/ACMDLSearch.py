from bs4 import BeautifulSoup as Soup
import requests as req

import sys, time

from Bkend import PaperClass

class ACM:
    def __init__(self, chunk=20, how_many=1):
        self.chunk = chunk
        self.pages = how_many
        self.search_URL = "https://dl.acm.org/action/doSearch"
        self.citation_URL = "https://dl.acm.org/action/exportCiteProcCitation"
        self.ENTRY_TYPE_Map = {"PAPER_CONFERENCE":'@inproceedings', "ARTICLE":'@article'}

    def __call__(self, **kwargs):
        self.query = kwargs['query']
        self.q = self.query.replace(' ', '+')
        bib_dict = self.browse_pages()
        return bib_dict

    def browse_pages(self):
        headers = {'User-Agent': 'Any', 'Content-Type': 'application/json'}
        params = {'AllField': self.q, 'pageSize': str(self.chunk), 'startPage': ''}
        res_dois = ''
        st = time.time()
        try:
            for i in range(0, self.pages):
                params['startPage'] = str(i)
                result_page_i = req.get(url=self.search_URL, headers = headers, params=params)
                res_dois_uns = Soup(result_page_i.text, 'html.parser').find_all(class_='issue-item__title')
                res_dois_uns = [res_doi.find('a').get('href')[5:] for res_doi in res_dois_uns]
                res_dois = ','.join(res_dois_uns) + ','
                ft = time.time()
                sys.stdout.write(
                    '\r Done visiting %s th ACM page - Collected %s items Time Elapsed: %.2fmin' % (
                        i + 1, (i + 1) * self.chunk, (ft - st) / 60))
            print()
            bibs = self.pluck_citations(res_dois)
            papers = self.organise_bibs(bibs)
        except:
            papers = None
        return papers

    def pluck_citations(self, res_dois):
        params = {"dois": res_dois,
                  "targetFile": "custom-bibtex",
                  "format": "bibtex"}
        bibs = req.get(url=self.citation_URL, params=params).json()['items']
        return bibs

    def organise_bibs(self, bibs):
        papers = []
        for cnt, item in enumerate(bibs):
            key = list(item.keys())[0]
            bib = item[key]
            authors = []
            auth_bib = ''
            for author in bib['author']:
                auth = author['given'] + ' ' + author['family']
                auth_bib += auth + ' and '
                authors.append(PaperClass.authorclass(auth))
            paper = PaperClass.paperclass(title=bib['title'], authors=authors,
                                          abstract=bib['abstract'], source='ACM-DL')
            paper.score.rank_source.append(('ACM-DL', len(bibs)-cnt))
            for key, value in bib.items():
                if key == 'author':
                    value = auth_bib[:-5]
                if type(value) is not str:
                    continue
                if key == 'id':
                    key = 'ID'
                if key == 'type':
                    key = 'ENTRYTYPE'
                    if value in self.ENTRY_TYPE_Map.keys():
                        value = self.ENTRY_TYPE_Map[value]
                    else:
                        value = '@misc'

                paper.attrs[key] = value
            papers.append(paper)
        return papers

# a = ACM()(query='query expansion using wordnet')
# for ass in a:
#     print(ass.bibify())