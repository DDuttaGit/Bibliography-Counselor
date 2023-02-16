#/usr/bin/python 
class core:
    def __init__(self, query):
        self.query = query
        
    def checkDupli(self, paper1, paper2):
        value = False
        if paper1.title == (paper2.title+"."):
            value = True
        
        return value 

merged = True
query = "wordnet query expansion"
sourceURL = "crossref";


if merged:
    import mergedSearch
    ms = mergedSearch.mergedSearch(query)
    mergedPapers = ms.msearch('dblp', 'ieee', 'acm')
    # mergedPapers = ms.msearch('dblp','ss')
    count = 0
    for mergedPaper in mergedPapers:
        print("merged sc: first title is "+str(mergedPaper.papers[0].title))
        print("first author is "+str(list(mergedPaper.papers[0].authors)[0].name))
        count = count + 1
    print("count ", count)
    for i in range(0, count-1):
        #print("i "+ str(i) + str(mergedPapers[i].papers[0].title))
        #print("i "+str(mergedPapers[i].papers[0].authors[0].name))
        for m in range(0,len(mergedPapers[i].papers)):
            #print("paper titles i=="+ str(m) + " " + str(mergedPapers[i].papers[m].title))
            for j in range(i+1, count):  
             #   print("ss")
                for n in range(0,len(mergedPapers[j].papers)):
                    #print("paper titles j=="+ str(n) + " " + str(mergedPapers[j].papers[n].title))
                    a = core(query)
                    same = False
                    # same = a.checkDupli(mergedPapers[i].papers[m], mergedPapers[j].papers[n])
                    same = mergedPapers[i].papers[m] == mergedPapers[j].papers[n] #m=15, n=17, query = "wordnet query expansion", dblp, crossref

                    if same:
                        print("same title", m, n);
                        dup_list.append((i, j, m, n))
    
    for dup_entry in dup_list:
        con1, con2, pap1, pap2 = dup_entry
        print(dup_entry)
        mergedPapers[con2].papers[pap2] = None
    unique_mergedPpapers = []
    for con in range(count):
        n_papers = []
        for paper in mergedPapers[con].papers:
            if paper is not None:
                n_papers.append(paper)
            else:
                print(paper)
        unique_mergedPpapers.append(n_papers)
          
else:
    import searchBase
    sb = searchBase.base(query)
    papers = sb.find_list(sourceURL)
    print(papers)





   

