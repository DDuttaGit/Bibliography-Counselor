#/usr/bin/python 
class base:
    def __init__(self, query):
        self.query = query
        

    
    def find_list(self, sourceURL, chunk=20):
        papers = [] 
        if sourceURL == 'DBLP':
            import DBLPSearch
            dsearch = DBLPSearch.dblp(self.query, chunk)
            papers = dsearch.search()
        
        elif sourceURL == 'Cross Ref':
            import crossRefSearch
            crsearch = crossRefSearch.crossref(self.query, chunk)
            papers = crsearch.search()
            
        elif sourceURL == 'Semantic Scholar':
            from SemanticScholar import SemanticScholar
            semanticsearch = SemanticScholar(chunk)
            papers = semanticsearch(query=self.query)
            
        elif sourceURL == 'IEEEXplore':
            from IEEESearch import IEEE
            ieeesearch = IEEE(chunk)
            papers = ieeesearch(query=self.query)
            
        elif sourceURL == 'ACM-DL':
            from ACMDLSearch import ACM
            acmsearch = ACM(chunk)
            papers = acmsearch(query=self.query)

        else:
            print("Biblio reference is not mentioned. Select sourceURL type. ")

        return papers
    
# query = "wordnet query expansion"
# papers = base(query).find_list('ieee')

