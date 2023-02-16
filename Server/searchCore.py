def make_search(query, sourceURLs, chunk=5):
    merged = len(sourceURLs) > 1
    # print(merged)
    if merged:
        import mergedSearch
        ms = mergedSearch.mergedSearch(query, chunk=chunk)
        mergedPapers, ordered_libraries = ms.msearch(sourceURLs)
        # mergedPapers = ms.msearch('dblp','ss')
        count = 0
        for mergedPaper in mergedPapers:
            # print(mergedPaper.papers[0])
            count = count + 1
        # print("No of Libraries: ", count)
        dup_list = []
        unique_papers = []
        for i in range(0, count-1):
            for m in range(0, len(mergedPapers[i].papers)):
                if mergedPapers[i].papers[m].score.rank_score is None:
                    continue
                for j in range(i+1, count):
                    for n in range(0, len(mergedPapers[j].papers)):
                        if mergedPapers[j].papers[n].score.rank_score is None:
                            continue
                        if mergedPapers[i].papers[m] == mergedPapers[j].papers[n]: #m=15, n=17, query = "wordnet query expansion", dblp, crossref
                            dup_list.append((i, j, m, n))
                            mergedPapers[i].papers[m].score.rank_source += mergedPapers[j].papers[n].score.rank_source
                            mergedPapers[j].papers[n].score.rank_score = None

        for dup_entry in dup_list:
            con1, con2, pap1, pap2 = dup_entry
            # print(mergedPapers[con2].papers[pap2])
            # print(dup_entry)

        for con in mergedPapers:
            for paper in con.papers:
                if paper.score.rank_score is not None:
                    unique_papers.append(paper)

        # print(len(dup_list),
        #       len(mergedPapers[0])+len(mergedPapers[1])+len(mergedPapers[2])+len(mergedPapers[3]))

        # for paper in unique_papers:
        #     print(paper, end='\n')
        return unique_papers, merged

    else:
        import searchBase
        sb = searchBase.base(query)
        papers = sb.find_list(sourceURLs)
        return papers, merged


'''
(0, 4, 0, 0)
(0, 1, 2, 3)
(0, 1, 3, 4)=========
(0, 3, 3, 0)=========
(0, 4, 3, 6)
(0, 1, 4, 3)
(0, 1, 6, 8)
(0, 1, 6, 11)
(0, 1, 8, 16)
(1, 2, 1, 4)
(1, 2, 2, 3)
(1, 3, 4, 0)==========
(1, 4, 4, 6)
(1, 2, 5, 0)
(1, 4, 7, 2)
(1, 3, 10, 2)
(1, 2, 12, 1)
(1, 4, 12, 4)
(1, 4, 13, 7)
(2, 4, 1, 4)
(3, 4, 0, 6)'''
