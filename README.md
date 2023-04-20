# Bibliography Counselor ![64_2](https://user-images.githubusercontent.com/52165986/219769891-905512cd-dfd0-4502-98ec-4f3e6daa7a5d.png)


_A Bibliographic Citation Recommendation System integrated with [Overleaf](https://www.overleaf.com)_

[![Build - Passing](https://img.shields.io/badge/Build-Passing-2ea44f)](https://github.com/DDuttaGit/Bibliography-Counselor/README.md) [![Extension - Chomium](https://img.shields.io/static/v1?label=Extension&message=Chomium&color=fa119f&logo=Google+Chrome)](https://) [![Extension - Gecko](https://img.shields.io/badge/Extension-Gecko-aeb44f?logo=Firefox)](https://addons.mozilla.org/en-US/firefox/addon/bibliography-counselor/)

Citation Recommendation is to provide bibliographic citation that a user is intending to fetch corresponding to a search query. This task differs from paper recommendation where it recommends documents that are worthwhile to read and to investigate. Survey publications have the sole objective to satisfy paper recommendation. __Bibliography Counselor__ is such a recommendation system integrated with __Overleaf__.

## Technical Specifications
This tool comes up with two front-end systems viz. a cross-browser extension and a PyQt based [local IDE](https://github.com/DDuttaGit/Bibliography-Counselor/tree/main/Local%20IDE) of which here we discuss about the work flow of the browser extension.

### Features

- Works seemlessly with Overleaf editor when the editor is ___Not___ in **Rich Text** mode.
- Chromium based extension is buit on _manifest version 3_ and [Gecko based extension](https://addons.mozilla.org/en-US/firefox/addon/bibliography-counselor/) has been deployed in manifest version 2 as gecko driver is still not that stable to manifest version 3.
    * Directory [Chromium Based Extension](https://github.com/DDuttaGit/Bibliography-Counselor/tree/main/Chromium%20Based%20Extension) provides the implementation for browsers like Google Chrome, Brave, Microsoft Edge etc.
    * Likewise, [Gecko Based Extension](https://github.com/DDuttaGit/Bibliography-Counselor/tree/main/Gecko%20Based%20Extension) provides the implementation for browsers like Firefox.
- Real-Time bibliography citation recommendation whre the pool of relevent documents are being collected from [ACM Digital Library](https://dl.acm.org/), [IEEE Xplore](https://ieeexplore.ieee.org/), [Semantic Scholar](https://www.semanticscholar.org/), [Crossref](https://www.crossref.org/) and [DBLP](https://dblp.org/).
- Uses **Borda Count** based positional voting for relevence calculation.
- **On-screen recommendation*" and **auto-population** of bibliography items and citations to proper place.
- User can have the choice to alter preferences.
- Keyboard Shortcut <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>S</kbd> and <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>U</kbd> are present to invoke the extension in chromium based and gecko based browsers respectively.
- Online [Server](https://github.com/DDuttaGit/Bibliography-Counselor/tree/main/Server) [^1] [^2]

### How to Run
1. After downloading the extension, install the extension by enabling developer mode in the browser.
2. Either use _keyboard shrortcut_ or open the options by _right click_ on the selected text in Overleaf editor.
3. Make preferences corresponding to each digital library.
4. Once the recommendations are fetched, select the items of ones choice.
5. Let the tool automatically copy your choices to the `*.bib` file and the bibliography citation keys after the selected text within the `\cite` command.

### Video demonstrating workflow in Brave browser

<!-- https://user-images.githubusercontent.com/52165986/219472699-f290b56d-e578-4ad6-ab49-ef6dbc60475a.mp4 -->


https://user-images.githubusercontent.com/52165986/219595267-43136366-1b93-4d30-ba25-bdc1e6a31a71.mp4


  
---

## Experimental Result
We have done our experiment and evaluated it on a self-deployed dataset. The experiment stems on online real time retrieval for which the results stated here may vary time-to-time depending upon the indexing of results in digital libraries over time.

Our collection of queries comprises the excerpts from the source files `*.tex` and `*.bib` submitted as [arXiv](https://arxiv.org/) pre-print. The format of a single record ___R___:
<div align='center'>

__R__ → _Id_ \`\n' __S__

__S__ → __QS<sub>1</sub>B__

__S<sub>1</sub>__ → __QS<sub>1</sub>B__  |  \`\n'

__Q__ →  ⟨an excerpt⟩ \` \$\$\$\$\$ '  ⟨Referrd bib key(s)⟩

__B__  →  ⟨Bibliography Record⟩ | ⟨Bibliography Record⟩__B__
</div>
where <i>Id</i> refer to an unique identity assigned to that record.


The evaluation is done in two environments viz.
1. __Strict Equality__: If retrieved document(s) is(are) exactly identical to the document(s) that has been cited by the author corresponding to that query then we term it as strict equality condition.
2. __Loose Equality__: However, we found instances where the cited document may not be retrieved by our backend query processor, but a significantly related document has been reported. By significantly related we mean the intersection between words of the title of a relevant and retrieved document is grater than a predefined threshold. In such a case we have also reduced the score of the retried document by a function dependent on the the intersection of words in the title of that retrieved document and the relevant document.

We have used _Trec eval_, an evaluation software dedicated to IR (Information Retrieval) system, to evaluate our results with the ground truth. 

|                  |  Strict Equality  |        |   Loose Equality  |        |
|------------------|:-----------------:|:------:|:-----------------:|--------|
| Digital Library  | Relevant Returned |   MAP  | Relevant Returned |   MAP  |
|              All |         7         | 0.1014 |         11        | 0.1353 |
|           ACM-DL |         4         | 0.0189 |         6         | 0.0254 |
| Semantic Scholar |         8         | 0.0962 |         11        | 0.0475 |
###### This table shows the result when our ground-truth text file contains 37 records __R__ which comprises 71 queries __Q__. The experiment has been done setting the _top-K_ = 5 documents retrieved from each library while collecting _top-k_ = 7 after ranking them using Weighted Borda Count. In addition to taking response from all  the digital libraries, we have also experimented separately on ACM-DL and Semantic Scholar.



[^1]: Because of serving from [AWS free-tier hosted machine](https://13.233.129.4/homepage.html); it lacks SSL certificate. Thus it will be necesssary to tell modern browsers to 'Proceed to Unsafe' in case there occures a `NET::ERR_CERT_AUTHORITY_INVALID` error.
[^2]: To keep a record to whom this webserver is serving, during recommendation it saves (as it runs in a limited credit) some details of requester viz. Overleaf account name, email and number of requests.
