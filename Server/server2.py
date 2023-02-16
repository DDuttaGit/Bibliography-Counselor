#!./MLib/bin/python3
print('Content-Type: text/html')
print('')
import cgi, SearchandRank, re, json, logging
def HTMLize(FlextoCatch, BibstoCatch):
    innerHTML = ''
    IDs = ''
    space = '&nbsp'*6
    i = 0
    for res, bib in zip(FlextoCatch, BibstoCatch):
        title, auth, src, scr, srcs = res.split('\n')[:-1]
        key = bib.split(',\n')[0].split('{')[-1]
        flex = '''<label style="display: inline-box; cursor:pointer; font-size:15px; color:#57798f; font-family: Lato, serif;">
        <input type="checkbox" id="bibitem_%d" value="%s">&nbsp&nbsp%s<br>%s%s<br>%s%s<br>%s%s<br>%s%s</label><div style="color: black; cursor:copy;">%sID: <tt>%s</tt></div><hr>'''%(i, bib, title, space, auth, space, src, space, scr, space, srcs, space, key)
        innerHTML += flex
        i += 1
    if innerHTML == '':
        innerHTML = '''No Results found. Sorry!! <a href="tel:+916289058997"> Call the Naive Dev </a>'''
    else:
        innerHTML = '<div id="result">'+innerHTML+'</div>'
    print(innerHTML)
    return innerHTML

def clean_query(query):
     pattern1 = r'\\(.*?)\{'
     pattern2 = r'\}'
     replacement = r''
     query = re.sub(pattern1, replacement, query)
     query = re.sub(pattern2, replacement, query)
     return query


form = cgi.FieldStorage()
val1 = clean_query(form.getvalue("q"))
val2 = int(form.getvalue("chunk"))
val3 = int(form.getvalue("top"))
acm = int(form.getvalue("acm")) if form.getvalue("acm") != None else 5
ieee = int(form.getvalue("ieee")) if form.getvalue("ieee") != None else 4
ss = int(form.getvalue("ss")) if form.getvalue("ss") != None else 3
crf = int(form.getvalue("crf")) if form.getvalue("crf") != None else 2
dblp = int(form.getvalue("dblp")) if form.getvalue("dblp") != None else 1

m = form.getvalue("m")
f = form.getvalue("f")
l = form.getvalue("l")
id = form.getvalue("id")
pid = form.getvalue("pi")
pn = form.getvalue("pn")
file = open('../userCred.json', 'r')
userCred = json.load(file)
if id not in userCred.keys():
    userCred[id] = {"first_name":f, "last_name":l, "email":m,"noofUses":0, "projects":{pid:{"pn":pn, "Uses":0}}}
userCred[id]["noofUses"] += 1
if pid not in userCred[id]["projects"].keys():
    userCred[id]["projects"][pid] = {"pn":pn, "Uses":0}
userCred[id]["projects"][pid]["Uses"] += 1
file.close()
with open('../userCred.json', 'w') as of:
    json.dump(userCred, of)

print(val1)
orderedLibs = {'ACM-DL': acm, 'IEEEXplore': ieee, 'Cross Ref': crf, 'DBLP': dblp, 'Semantic Scholar': ss}
ret = SearchandRank.run(val1, orderedLibs, val2, val3)
if len(ret) == 1:
    print('<p>Something has gone Wrong'+e+'</p>')
else:
    T, B = ret[0], ret[1]
    print('<br><br>')
    HTMLize(T, B)
