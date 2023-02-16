query = "Query Expansion using Wordnet"
orderedLibs = {'ACM-DL': 5, 'IEEEXplore': 4, 'Cross Ref': 3, 'DBLP': 2, 'Semantic Scholar': 1}

def run(query, orderedLibs, chunk, top):
    FlextoCatch = []
    BibstoCatch = []

    import searchCore, rank_fusion

    sourceURLs = list(orderedLibs.keys())
    try:
        papers, merged = searchCore.make_search(query, sourceURLs,chunk=chunk)
        if papers is not None:
            if merged:
                papers = rank_fusion.borda_count(papers, orderedLibs, top)
                for paper in papers:
                    FlextoCatch.append(paper.__str__())
                    BibstoCatch.append(paper.bibify())
        return FlextoCatch, BibstoCatch
    except:
        #print('Search Method throws an Exception')
        return 'Search Method throws an Exception'

# print(run(query, orderedLibs, 5, 5))
