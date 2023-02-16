import requests as req

import sys, time
import bibtexparser

import PaperClass

class IEEE:
    def __init__(self, chunk=20, how_many=1):
        self.chunk = chunk
        self.pages = how_many
        self.search_URL = "https://ieeexplore.ieee.org/rest/search"
        self.citation_URL = "https://ieeexplore.ieee.org/xpl/downloadCitations"

    def __call__(self, **kwargs):
        self.query = kwargs['query']
        self.q = '(' + '\\"' + 'All Metadata' + '\\":' + self.query + ')'
        self.q = '\"' + self.q + '\"'
        bib_dict = self.browse_pages()
        return bib_dict


    def browse_pages(self):
        data = '''{"action":"search",
                      "newsearch":true,
                      "matchBoolean":true,
                      "queryText":''' + self.q + ''',
                      "returnType":"SEARCH",
                      "rowsPerPage":''' + str(self.chunk) + ','
        headers = {
            'Content-Type': 'application/json',
            'Origin': 'https://ieeexplore.ieee.org',
        }
        st = time.time()
        bibs = ''
        try:
            for i in range(0, self.pages):
                data += '''"pageNumber":''' + str(i) + '}'
                result_page_i = req.post(self.search_URL, headers=headers, data=str(data)).json()
                ieee_papers = result_page_i['records']
                paper_ids = [paper['documentLink'].split('/')[-2] for paper in ieee_papers]
                paper_ids = ','.join(paper_ids)
                ft = time.time()
                sys.stdout.write(
                    '\r Done visiting %s th IEEE page - Collected %s items Time Elapsed: %.2fmin' % (
                    i + 1, (i + 1) * self.chunk, (ft - st) / 60))
                bibs += self.pluck_citations(paper_ids)
            print()
            papers = self.organize_bibs(bibs)
        except:
            papers =None
        return papers

    def pluck_citations(self, paper_ids):
        params = {"recordIds": paper_ids,
                  "citations-format": "citation-&-abstract",
                  "download-format": "download-bibtex"}
        bibs = req.get(url=self.citation_URL, params=params).text
        bibs = bibs.replace('<br>', '').replace('<br/>', '\n')
        bibs = bibs.replace('},}', '},}\n\n')
        bibs = bibs.replace(',\r\n\r\nauthor=', ',\nauthor=')
        return bibs

    def organize_bibs(self, bibs):
        bib_database = bibtexparser.loads(bibs)
        papers = []
        for cnt, bib in enumerate(bib_database.entries, start=0):
            bib = bibtexparser.customization.author(bib)
            authors = []
            auth_bib = ''
            for author in bib['author']:
                family, given = author.split(',')
                auth_bib += given+ ' ' + family + ' and '
                author = PaperClass.authorclass(given+ ' ' + family)
                authors.append(author)
            paper = PaperClass.paperclass(title=bib['title'], authors=authors,
                                          abstract=bib['abstract'], source='IEEEXplore')
            paper.score.rank_source.append(('IEEEXplore', len(bib_database.entries) - cnt))
            for key, value in bib.items():
                if key == 'author':
                    value = auth_bib[:-5]
                if type(value) is not str:
                    continue
                if key == 'ENTRYTYPE':
                    value = '@'+value
                paper.attrs[key] = value
            papers.append(paper)
        return papers

# a = IEEE()(query='query expansion using wordnet')
# for ass in a:
#     print(ass.bibify())
# with open('j.json', 'w') as f:
#     json.dump(bibs, f)