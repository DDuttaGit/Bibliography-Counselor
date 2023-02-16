'''
Created on 03-Feb-2022

@author: dipa
'''
class mergedSearch:
    def __init__(self, query, chunk=20):#, *sourceURLs):
        self.query = query
        self.chunk = chunk

    def msearch(self, sourceURLs):

        import searchBase
        import PaperClass
        sc = searchBase.base(self.query)
        mergedPapers = []
        for cnt, sourceURL in enumerate(sourceURLs):
            print("Searched: " + sourceURL)
            papers = sc.find_list(sourceURL, self.chunk)
            if papers is None or len(papers) == 0:
                print(sourceURL + ' did not return valid result')
            else:
                mergedPapers.append(PaperClass.allpapers(papers))
            # if cnt == 0:
            #     a = attrs
            # else:
            #     a = a.intersection(attrs)
        # print(type(sourceURLs))
        return mergedPapers, sourceURLs

