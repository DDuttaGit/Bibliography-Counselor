#/usr/bin/python 

punctuations = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'

class score:
    def __init__(self):
        self.rank_score = 0
        self.rank_source = []
        self.data_score = 0

    def __str__(self):
        return "%d\nSources: %s"%(self.rank_score, self.rank_source)

class authorclass:
    def __init__(self, name):
        self.name = name.strip(' ')

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        sn = self.name.split(' ')
        sng, snf = (sn[0][0].lower(), sn[-1])
        on = other.name.split(' ')
        ong, onf = (on[0][0].lower(), on[-1])
        return sng == ong and snf == onf


class paperclass:
    def __init__(self, title, authors, source, abstract=''):
        self.title = title.strip(' ')
        self.authors = authors
        self.score = score()
        self.abstract = abstract
        self.attrs = {}
        self.source = source

    def __str__(self):
        self.str = "Title: %s \nAuthors: %s\nMnSource: %s\nScore: %s\n"%(self.title, self.authors,
                                                                         self.source, self.score.__str__())
        return self.str

    def __eq__(self, other):
        t1 = self.title.lower()
        t1 = t1.translate(str.maketrans('', '', punctuations))
        t2 = other.title.lower()
        t2 = t2.translate(str.maketrans('', '', punctuations))
        return t1 == t2 and \
               self.authors == other.authors

    def bibify(self):
        bib_dict = self.attrs
        bibstr = bib_dict['ENTRYTYPE'] + '{' + bib_dict['ID'] + ',\n'
        for key, value in bib_dict.items():
            if key != 'ENTRYTYPE' and key != 'ID' and key != 'abstract':
                bibstr += key + ': ' + value + ',\n'
        bibstr += '}\n'
        return bibstr

class allpapers:
    def __init__(self, papers):
        self.papers = papers

    def __len__(self):
        return len(self.papers)