#/usr/bin/python 
class base:
    def __init__(self, query):
        self.query = query
        

    
    def find_list(self, sourceURL, chunk=20):
        papers = [] 
        if sourceURL == 'DBLP':
            from Bkend import DBLPSearch
            dsearch = DBLPSearch.dblp(self.query, chunk)
            papers = dsearch.search()
        
        elif sourceURL == 'Cross Ref':
            from Bkend import crossRefSearch
            crsearch = crossRefSearch.crossref(self.query, chunk)
            papers = crsearch.search()
            
        elif sourceURL == 'Semantic Scholar':
            from Bkend import SemanticScholar
            semanticsearch = SemanticScholar.SemanticScholar(chunk)
            papers = semanticsearch(query=self.query)
            
        elif sourceURL == 'IEEEXplore':
            from Bkend import IEEESearch
            ieeesearch = IEEESearch.IEEE(chunk)
            papers = ieeesearch(query=self.query)
            
        elif sourceURL == 'ACM-DL':
            from Bkend import ACMDLSearch
            acmsearch = ACMDLSearch.ACM(chunk)
            papers = acmsearch(query=self.query)

        else:
            print("Biblio reference is not mentioned. Select sourceURL type. ")

        return papers
    
# query = "wordnet query expansion"
# papers = base(query).find_list('ieee')

