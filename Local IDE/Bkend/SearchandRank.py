from Bkend import searchCore, rank_fusion

def run(query, sourceURLs, top, printer):
    papers, merged = searchCore.make_search(query, sourceURLs,chunk=5)
    if merged:
        rank_fusion.borda_count(papers, sourceURLs, top, printer)
