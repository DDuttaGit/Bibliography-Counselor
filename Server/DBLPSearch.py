#/usr/bin/python


class dblp:
    def __init__(self, query, chunk=20):
        self.query = query.replace(' ', '+')
        self.chunk = chunk
        self.ENTRY_TYPE_Map = {"Conference and Workshop Papers":'@inproceedings', "Journal Articles":'@article'}

    def search(self):
        from requests import get
        
        self.url = "https://dblp.uni-trier.de/search/publ/api?q="+self.query+"&format=json&h="+str(self.chunk)
        response = get(self.url).json()
        result = response['result']
        status = result['status']['text']
        import PaperClass
        papers = [] 
        if status == 'OK':
            try:
                paprs = result['hits']['hit']
                for cnt, papr in enumerate(paprs):
                    papr = papr['info']
                    authors = []
                    auth_bib = ''
                    for author in papr['authors']['author']:
                        authors.append(PaperClass.authorclass(author['text']))
                        auth_bib += author['text'] + ' and '
                    paper = PaperClass.paperclass(title=papr['title'], source='DBLP',authors=authors)
                    paper.score.rank_source.append(('DBLP', len(paprs)-cnt))
                    for key, value in papr.items():
                        if key == 'authors':
                            value = auth_bib[:-5]
                            key = 'author'
                        if type(value) is not str:
                            continue
                        if key == 'key':
                            key = 'ID'
                        if key == 'type':
                            key = 'ENTRYTYPE'
                            if value in self.ENTRY_TYPE_Map.keys():
                                value = self.ENTRY_TYPE_Map[value]
                            else:
                                value = '@misc'
                        paper.attrs[key] = value
                    papers.append(paper)
            except:
                print('Exception at DBLP')
                papers = None
        else:
            print("dblp not found")

        return papers

# a = dblp(query='query expansion using wordnet').search()
#
# for ass in a:
#     print(ass.bibify())
