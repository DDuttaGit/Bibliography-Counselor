import requests as req

import sys, time

import PaperClass

class SemanticScholar:
    def __init__(self, chunk=20, how_many=1):
        self.chunk = chunk
        self.pages = how_many
        self.search_and_citation_URL = "https://api.semanticscholar.org/graph/v1/paper/search"

    def __call__(self, **kwargs):
        self.query = kwargs['query']
        self.q = self.query
        bib_dict = self.browse_pages()
        return bib_dict

    def browse_pages(self):
        headers = {'User-Agent': 'Any', 'Content-Type': 'application/json'}
        params = {'query': self.q, 'fields':'title,abstract,authors,venue',
                  'limit':str(self.chunk)}
        res_data = []
        st = time.time()
        try:
            for i in range(0, self.pages):
                params['offset'] = str(self.chunk*(i))
                result_page_i = req.get(url=self.search_and_citation_URL, headers = headers, params=params).json()
                ft = time.time()
                sys.stdout.write(
                    '\r Done visiting %s th Semantic Scholar page - Collected %s items Time Elapsed: %.2fmin' % (
                        i + 1, (i + 1) * self.chunk, (ft - st) / 60))
                res_data += result_page_i['data']
            print()
            papers = self.organise_bibs(res_data)
        except:
            papers = None
        return papers

    def organise_bibs(self, bibs):
        papers = []
        for cnt, bib in enumerate(bibs):
            authors = []
            auth_bib = ''
            for author in bib['authors']:
                auth = author['name']
                auth_bib += auth + ' and '
                authors.append(PaperClass.authorclass(auth))
            paper = PaperClass.paperclass(title=bib['title'], authors=authors,
                                          abstract=bib['abstract'], source='Semantic Scholar')
            paper.score.rank_source.append(('Semantic Scholar', len(bibs)-cnt))
            for key, value in bib.items():
                if key == 'authors':
                    value = auth_bib[:-4]
                    key = 'author'
                if type(value) is not str:
                    continue
                paper.attrs[key] = value
                paper.attrs['ENTRYTYPE'] = '@misc'
                paper.attrs['ID'] = bib['paperId']
            papers.append(paper)
        return papers

# a = SemanticScholar()(query='query expansion using wordnet')
# for ass in a:
#     print(ass.bibify())
# with open('k.json', 'w') as f:
#     json.dump(a, f)
