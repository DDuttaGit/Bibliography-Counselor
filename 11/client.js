SERVER_URL =  "https://13.233.129.4/"
function BibHandler(Query, Dict, Wait)
{
    message = '?q='+Query+'&';
    userCred = JSON.parse(document.getElementsByName('ol-user')[0].content);
    Dict["f"] = userCred['first_name'];
    Dict["l"] = userCred['last_name'];
    Dict["id"] = userCred['id'];
    Dict["m"] = userCred['email'];
    Dict['pi']  = document.getElementsByName('ol-project_id')[0].content;
    Dict['pn'] = document.getElementsByName('ol-projectName')[0].content;
    for (const [key, value] of Object.entries(Dict)) {
        message += key+'='+value+'&';
    }
    message = message.slice(0,-1);
    fetch(SERVER_URL+'cgi-bin/server2.py'+message)
  .then((response) => response.text())
  .then((data) => {
    var parser = new DOMParser();
	var doc = parser.parseFromString(data, 'text/html');
    // console.log(data);
	d = doc.body.getElementsByTagName('div')[0].innerHTML;
    injectNativeModalContent(Wait, d, Query);
    if (!Wait)
            clearInterval(intervalID);})
   .catch((data) => {
    injectNativeModalContent(Wait, 'Error Occurred at Server'+data, Query);
    if (!Wait)
        clearInterval(intervalID);
    });

    if (!Wait)
        intervalID = loading(Query);
}
