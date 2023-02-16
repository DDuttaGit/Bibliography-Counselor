def borda_count(unique_papers, ordered_library, top, printer):
    lib_cnt = len(ordered_library)
    for paper in unique_papers:
        for scores in paper.score.rank_source:
            lib, rank = scores[0], scores[1]
            imp_lib = lib_cnt - ordered_library.index(lib)
            paper.score.rank_score += imp_lib*rank
    unique_papers.sort(key=lambda paper: paper.score.rank_score, reverse=True)
    for paper in unique_papers:
        printer.print_(paper.__str__())
        printer.print_(paper.bibify())
    return unique_papers[:top]


'''voters = ['3', '2', '1']

preferences = {'3': ['C', 'B', 'D', 'E', 'A'],
               '2': ['A', 'C', 'D', 'B', 'E'],
               '1': ['D', 'A', 'E', 'C', 'B']}

def borda(preferences):
    for voter, pref in preferences.items():
        for cnt, pre in enumerate(pref):
            candidates[pre] += (len(pref) - cnt)*int(voter)
    print(candidates)


Merged_Papers = {'A':0, 'B':0, 'C':0, 'D':0, 'E':0, 'F':0}

Library_Imp = {'ACM':3, 'IEEE': 2, 'Crossref':1}

RankedListfromLibraies = {'ACM': ['B', 'D', 'E', 'C', 'A'],
                          'IEEE': ['E', 'A', 'B', 'C', 'F'],
                          'Crossref': ['A', 'F', 'C', 'B', 'E']}

for lib, paper_list in RankedListfromLibraies.items():
    for cnt, paper in enumerate(paper_list):
        Merged_Papers[paper] += (len(paper_list)-cnt) * Library_Imp[lib]

print(Merged_Papers)
'''