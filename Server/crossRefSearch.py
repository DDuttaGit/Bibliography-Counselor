#/usr/bin/python

def listToString(s): 
    
    str1 = "" 
    
    for ele in s: 
        str1 += ele  
    
    return str1 
 
class crossref:
    def __init__(self, query, chunk=20):
        self.query = query
        self.chunk = chunk
        self.ENTRY_TYPE_Map = {"proceedings-article":'@inproceedings', "journal-article":'@article'}


    def search(self):
        from bs4 import BeautifulSoup
        from requests import get
        import re
        import json
        
        self.url = re.sub("%query%", self.query, "https://api.crossref.org/works?query=%query%")
        self.url = self.url+'&rows='+str(self.chunk)
        # urlmod = self.url+"&mailto=%query%"
        # mailAdd = "dipasree.pal@gmail.com"
        # self.url = re.sub("%query%", mailAdd, urlmod)

        try:
            response = get(self.url)

            html_soup = BeautifulSoup(response.text, 'html.parser')
            obj = json.loads(html_soup.text)
            import PaperClass
            papers = []
            if obj["status"] == 'ok':
                for cnt, i in enumerate(obj['message']['items']):
                    title = listToString(i['title'])
                    if 'abstract' in i.keys():
                        abs = i['abstract']
                    else:
                        abs = None
                    authors = []
                    if not (i.get('author') is None):
                        k = 0
                        auth_bib = ''
                        for j in i['author']:
                            if "given" in j.keys():
                                authors.append(PaperClass.authorclass(j['given']+" "+j['family']))
                                auth_bib += j['given']+" "+j['family'] + ' and '
                            else:
                                authors.append(PaperClass.authorclass(j['family']))
                                auth_bib += j['family'] + ' and '
                            k = k + 1
                    paper = PaperClass.paperclass(title=title, authors=authors, source='Cross Ref', abstract=abs)
                    paper.score.rank_source.append(('Cross Ref', len(obj['message']['items']) - cnt))
                    for key, value in i.items():
                        if key == 'author':
                            value = auth_bib[:-5]
                        if type(value) is not str:
                            continue
                        if key == 'type':
                            key = 'ENTRYTYPE'
                            if value in self.ENTRY_TYPE_Map.keys():
                                value = self.ENTRY_TYPE_Map[value]
                            else:
                                value = '@misc'
                        paper.attrs[key] = value
                        title = listToString(i['title'])
                        paper.attrs['title'] = title
                        try:
                            paper.attrs['ID'] = i['DOI']
                        except:
                            paper.attrs['ID'] = title.split(' ')[0]+title.split(' ')[1]
                    papers.append(paper)

            else:
                print("crossref not found")
        except:
            papers = None
        return papers

# a = crossref(query='I know the moment I have overlooked some details').search()
# for ass in a:
    # print(ass.bibify())

