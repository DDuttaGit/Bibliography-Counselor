/*================================================================================*/
/* -------------------------code: sub of world: "MAIN"----------------------------*/
/*================================================================================*/
    
var actualCode = '(' + PerformDOMOperation + ')();';
var script = document.createElement('script');
script.textContent = actualCode;
(document.head||document.documentElement).appendChild(script);
script.remove();


/*================================================================================*/
/* -------------------------File: run.js------------------------------------------*/
/*================================================================================*/
    
PerformDOMOperation();

function PerformDOMOperation()
{
    if (! document.URL.startsWith('https://www.overleaf.com/project/'))
    {
        if (window.confirm('ERROR: You Should be in some Overleaf Projects. Redirect to Overleaf')) 
            window.location.href='https://www.overleaf.com/project/';   
    }
    else
    {
        Query = queryExtractor();
        if (Query !== '')
            getChoiceModal(Query);
        else
            injectNativeModalNoCite();
    }

    /*================================================================================*/
    /* -------------------------File: chooseEditor.js---------------------------------*/
    /*================================================================================*/
    var cm6_f, cm6_t;
    function queryExtractor()
    {
        editortype = _ide.editorManager.getEditorType();
        if(editortype === 'ace')
        {
            if(!_ide.editorManager.$scope.editor.sharejs_doc.ace.session.getSelection().$isEmpty)
            {
                anchor = _ide.editorManager.$scope.editor.sharejs_doc.ace.session.getSelection().anchor
                cursor = _ide.editorManager.$scope.editor.sharejs_doc.ace.session.getSelection().cursor
                if (anchor['row'] > cursor['row']){
                    tmp = anchor;
                    anchor = cursor;
                    cursor = tmp;
                }
                else if (anchor['row'] === cursor['row'] && anchor['column'] > cursor['column']){
                    tmp = anchor;
                    anchor = cursor;
                    cursor = tmp;
                }
                st_r = anchor['row'];
                fn_r = cursor['row'];
                st_c = anchor['column'];
                fn_c = cursor['column'];
                lines = _ide.editorManager.$scope.editor.sharejs_doc.ace.session.getLines(st_r, fn_r);
                if(st_r !== fn_r)
                {
                    lines[0] = lines[0].slice(st_c);
                    lines[lines.length - 1] = lines[lines.length - 1].slice(0, fn_c);
                }
                else
                    lines[0] = lines[0].slice(st_c, fn_c);
                Query = '';
                for(i=0; i<lines.length; i++)
                    Query += lines[i] + ' ';
                return Query.slice(0,-1);
            }
            else
                return '';
        
        }

        else if(editortype === 'cm6')
        {
            var cm6ide = _ide.editorManager.$scope.editor.sharejs_doc.cm6
            var selected = cm6ide.view.state.selection
            cm6_f = selected['ranges'][0]['from']
            cm6_t  = selected['ranges'][0]['to']
            return cm6ide.getValue().slice(cm6_f, cm6_t).replace('\n', ' ').trim()
            
        }
        else return '';
    }


    /*================================================================================*/
    /* -------------------------File: user.js-----------------------------------------*/
    /*================================================================================*/
    function getChoiceModal(Query)
    {
        if (document.getElementById("CouncillorUserMdal") === null)
        {
            var mdalDialog = document.createElement('div');
            mdalDialog.role = "dialog";
            mdalDialog.id = "CouncillorUserMdal";
            mdalDialog.innerHTML = 
            `<div class="fade modal-backdrop in"></div>
            <div role="dialog" tabindex="-1" class="fade in modal" style="display: block; id=mdal-frame">
                <div class="modal-dialog">
                    <div class="modal-content" role="document">
                        <div class="modal-header">
                            <button type="button" class="close" id="userClose">&times</button>
                            <h4 class="modal-title">Your Search Query: ${Query}</h4>
                        </div>
                        <div class="modal-body" id="mbdy-userChoice">
                        <label style="display: inline-box; cursor:pointer;">
                            <input type="checkbox" checked="true" id="userChoiceCBox">
                            Go with Default Settings
                        </label><br>
                        <label style="display: inline-box; cursor:pointer;">
                            <input type="checkbox" id="userWaitCBox">
                            I Don't like to Wait
                        </label><br>
                        </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-info" id="mdal-ok">Ok</button>
                            </div>
                        </div>
                    </div>
                </div>`
            document.body.appendChild(mdalDialog);
            injectUserChoiceModalScript(Query);
        }
    }

    function injectUserChoiceModalScript(Query)
    {
        if (document.getElementById("CouncillorUserMdal") !== null)
        {
            var mdal = document.getElementById("CouncillorUserMdal")
            var mdlOk = document.getElementById("mdal-ok");
            var mdluserClose = document.getElementById("userClose");
            
            cbox = document.getElementById("userChoiceCBox");
            mdlOk.onclick = function() { 
                Wait = document.getElementById("userWaitCBox").checked;
                if(!cbox.checked)
                {
                    var mdalBdy = document.getElementById("mbdy-userChoice");
                    mdalBdy.innerHTML =`<table style="border-collapse: separate; border-spacing: 0 0.5em;">
                            <tr>
                            <th>DigLib</th>
                            <th>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp</th>
                            <th>Score</th>
                            </tr>
                            <tr>
                            <td><label for="ACM-DL">ACM-DL</label></td>
                            <td><span>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp</span></td>
                            <td><input class="form-control" type="number" id="acm" value=5></td>
                            </tr>
                            <tr>
                            <td><label for="IEEE">IEEEXplore</label></td>
                            <td><span>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp</span></td>
                            <td><input class="form-control" type="number" id="ieee" value=4></td>
                            </tr>
                            <tr>
                            <td><label for="Cross Ref">Cross Ref</label></td>
                            <td><span>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp</span></td>
                            <td><input class="form-control" type="number" id="crf" value=3></td>
                            </tr>
                            <tr>
                            <td><label for="DBLP">DBLP</label></td>
                            <td><span>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp</span></td>
                            <td><input class="form-control" type="number" id="dblp" value=2></td>
                            </tr>
                            <tr>
                            <td><label for="Semantic Scholar">Semantic Scholar</label></td>
                            <td><span>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp</span></td>
                            <td><input class="form-control" type="number" id="ss" value=1></td>
                            </tr>
                            <tr>
                            <td><input class="form-control" type="number" id="chunk" placeholder='Chunk' value="5" title='Chunks to Recieve from each Lib'></td>
                            <td><span>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp</span></td>
                            <td><input class="form-control" type="number" id="top" placeholder='Top-K' value="5" title='Top k to return'></td>
                            </tr>
                            <tr>
                            <td><label for="Search Method">Search Method</label></td>
                            <td><span>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp</span></td>
                            <td><select class="form-control input-sm"><option>Borda Count</option></select></td>
                            </tr>
                        </table>` ;
                    mdlOk.innerHTML = 'Search Bibs';
                    mdlOk.onclick = function() {
                        Dict = pickChoices(mdalBdy);
                        mdal.remove();
                        BibHandler(Query, Dict, Wait);
                    }
                }
                else
                {
                    mdal.remove();
                    Dict = {"acm": "5", "ieee": "4", "crf": "3", "dblp": "2", "ss": "1", "chunk": "5", "top": "5"};
                    BibHandler(Query, Dict, Wait);
                }
            }
            
            mdluserClose.onclick = function()
            {
                mdal.remove();
            }
        }
    }

    function pickChoices(Body)
    {
        inputs = Body.getElementsByTagName('input');
        Dict = {};
        for (i=0; i<inputs.length; i++)
            Dict[inputs[i].id] = inputs[i].value;
        return Dict;
    }



    /*================================================================================*/
    /* -------------------------File: action.js---------------------------------------*/
    /*================================================================================*/
    function injectNativeModal(Query)
    {
        if (document.getElementById("CouncillorMdal") === null)
        {
            var mdalDialog = document.createElement('div');
            mdalDialog.role = "dialog";
            mdalDialog.id = "CouncillorMdal";
            mdalDialog.innerHTML = 
            `<div class="fade modal-backdrop in"></div>
            <div role="dialog" tabindex="-1" class="fade in modal" style="display: block; id=mdal-frame">
                <div class="modal-dialog">
                    <div class="modal-content" role="document">
                        <div class="modal-header">
                            <h4 class="modal-title">Your Search Query: ${Query}</h4>
                        </div>
                        <div class="modal-body" id="mbdy"></div>
                        <div class="modal-footer" id="mftr">
                            <button type="button" class="btn btn-default" id="mdal-close">Cancel</button>
                            <button type="button" class="btn btn-primary" style="cursor: copy;" id="mdal-copy">Copy</button>
                        </div>
                    </div>
                </div>
            </div>`
            document.body.appendChild(mdalDialog);
        }
    }

    function injectNativeModalScript()
    {
        if (document.getElementById("CouncillorMdal") !== null)
        {
            var mdal = document.getElementById("CouncillorMdal")
            var mdlCls = document.getElementById("mdal-close");
            mdlCls.onclick = function() { 
                mdal.remove();
            }
            
            var mdlCpy = document.getElementById("mdal-copy"); 
            mdlCpy.onclick = function()
            {
                if (document.getElementById('mbdy').innerHTML !== ' ')
                {
                    bibToCopy = '';
                    bibIDstoCopy = '';
                    bibCount = document.getElementById('mbdy').getElementsByTagName('label').length;
                    IDs = document.getElementById('mbdy').getElementsByTagName('tt');
                    for (i=0; i<bibCount; i++) 
                    { 
                        bibItem = document.getElementById('bibitem_'+i.toString()); 
                        if (bibItem.checked)
                        { 
                            bibToCopy += bibItem.value+'\n\n';
                            bibIDstoCopy += IDs[i].innerHTML + ', ';
                        }
                    }
                    bibIDstoCopy = bibIDstoCopy.slice(0, -2);
                    mdlCpy.innerHTML = 'Copied!';
                    mdlCls.innerHTML = 'Done';
                    citebibfind(bibToCopy, bibIDstoCopy);
                }
            }
        }
    }

    function injectNativeModalContent(Wait, data, Query)
    {
        // Script Generating Modal content containg Bibs
        if (!Wait)
        {
            if (document.getElementById("CouncillorMdal") !== null)
            {
                // if (document.getElementById('mbdy').innerHTML === '')
                if (document.getElementById("Loading at Councillor") !== null)
                {
                    document.getElementById("OutlayerLoading").remove();
                    var container = document.getElementById('mbdy');
                    var conatiner_ftr = document.getElementById('mftr');
                    userCred = JSON.parse(document.getElementsByName('ol-user')[0].content)
                    u = "Access by: " + userCred['first_name'] + " " + userCred['last_name'] + " (" + userCred['email'] + ")" + " having user ID: " + userCred['id'];
                    container.innerHTML = data + "<p>" + u + "</p>";
                }
            }
        }

        else if(Wait)
        {
            injectNativeModal(Query);
            injectNativeModalScript();
            var container = document.getElementById('mbdy');
            container.innerHTML = data;
        }
    }

    function loading(Query)
    {
        injectNativeModal(Query);
        injectNativeModalScript();
        // time = wtTime;
        document.getElementById('mbdy').innerHTML = `
            <div class="loading-screen ng-scope" ng-if="state.loading" id="OutlayerLoading">
                <div class="loading-screen-brand-container">
                    <div class="loading-screen-brand" style="height: 0%;" id="Loading at Councillor" ng-style="{ 'height': state.load_progress + '%' }"></div>
                </div>
                <!-- ngIf: !state.error -->
                <!-- ngIf: state.error -->
                <p class="loading-screen-error ng-scope" ng-if="state.error">
                    <span ng-bind-html="state.error" class="ng-binding" id="biberror"></span>
                </p>
                <!-- end ngIf: state.error -->
            </div>`
        var intervalID = setInterval(function(){
            arr = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100];
            randomIndex = Math.floor(Math.random() * arr.length);
            item = arr[randomIndex];
            var load = document.getElementById("Loading at Councillor");
            if (load !== null)
            {
                load.setAttribute("style", "height: "+item.toString()+"%");
                er = document.getElementById("biberror");
                if (er !== null)
                {
                    // er.innerHTML = 'Your Expected Wait Time: '+time.toString() + ' sec';
                    er.innerHTML = 'Usual Wait Time is (7, 22) sec <br> Please wait that long<br> For longer than that Please Reload this Page';
                }
                // console.log(intervalID);
            }
            
        }, 1000);
        // clearInterval(intervalID); ==> Done in Client after recieve
        return intervalID;
    }

    function injectNativeModalNoCite()
    {
        if (document.getElementById("CouncillorNoCitMdal") === null)
        {
            editortype = _ide.editorManager.getEditorType();
            if (editortype==='ace')
                msg = `<div class="modal-body" style="background-color: #3a4454" id="mbdy"><h4 class="modal-title" style="color: white">No Query found<hr>General Format:&nbsp&nbsp&nbsp <tt>Just make a Selection</tt></h4></div>`;
            else if(editortype === 'cm6')
                msg = `<div class="modal-body" style="background-color: #3a4454" id="mbdy"><h4 class="modal-title" style="color: white">No Query found<hr>General Format:&nbsp&nbsp&nbsp <tt>Make a Selection of a Query</tt></h4></div>`;
                // msg = `<div class="modal-body" style="background-color: #3a4454" id="mbdy"><h4 class="modal-title" style="color: white">No Query found<hr>General Format:&nbsp&nbsp&nbsp <tt> \\scite <u><strong>Query String</strong></u> \\cite</tt></h4></div>`;
            else
                msg = `<div class="modal-body" style="background-color: #3a4454" id="mbdy"><h4 class="modal-title" style="color: white">No Query found<hr>You are either in the page where all your Projects are listed<br><br><u>OR</u><br><br> In such an editor (Rich Text) where we currently don't Provide a service.</h4></div>`;
            var mdalDialog = document.createElement('div');
            mdalDialog.role = "dialog";
            mdalDialog.id = "CouncillorNoCitMdal";
            mdalDialog.innerHTML = `<div class="fade modal-backdrop in"></div>
            <div role="dialog" tabindex="-1" class="fade in modal" style="display: block; id=mdal-frame">
                <div class="modal-dialog">
                    <div class="modal-content" role="document">` + msg + 
                            `<div class="modal-footer" style="background-color: #3a4454">
                                <button type="button" class="btn btn-default" id="mdal-cancel">Try Again</button>
                            </div>
                        </div>
                    </div>
                </div>`
            
            document.body.appendChild(mdalDialog);
            var mdalNoCit = document.getElementById("CouncillorNoCitMdal");
            var mdlCanc = document.getElementById("mdal-cancel");
            mdlCanc.onclick = function() { mdalNoCit.remove();}
        }
    }

    function citebibfind(data, id)
    {
        Done = document.getElementById('mdal-close');
        Copied = document.getElementById('mdal-copy');
        Done.disabled = true;
        Copied.disabled = true;
        ftr = document.getElementById('mftr');
        fileTree = document.getElementsByClassName("list-unstyled file-tree-list")[0];
        files = fileTree.getElementsByTagName('li');
        bibFound = 0;
        for(i=0; i<files.length; i++)
        {
            bibFile = files[i].getAttribute("aria-label");
            if (bibFile!== null && bibFile.toString().endsWith(".bib"))
                {btn = files[i].getElementsByTagName('button')[0];
                bibFound = 1;}
            if (bibFile!== null && files[i].getAttribute("class") === "selected")
            {
                prebtn = files[i].getElementsByTagName('button')[0];
                if(_ide.editorManager.getEditorType() === 'ace')
                    cursor = knowAnchorCursor();
            }
        }
        if (bibFound === 0)
        {
            newFile = document.getElementsByClassName("toolbar-left")[1].getElementsByTagName("button")[0];
            newFile.click();
            buttons = document.getElementsByTagName('button');
            input = document.getElementById("new-doc-name");
            _ide.showGenericMessageModal('No Bib file found in File Tree', `On next UI please give a suitable name of the Bib file`);
            // input.dispatchEvent(new Event('input', { bubbles: true }));
            buttons[buttons.length-1].onclick = function() {myFunction()};
            buttons[buttons.length-2].onclick = function() {closeEverything()};
            function myFunction() {
                setTimeout(function(){citebibfind(data, id)}, 1000);
            }
            function closeEverything(){
                document.getElementById('CouncillorMdal').remove();
                _ide.showGenericMessageModal('Everything Destroyed', 'You did not create a bib file!!');
            }
        }
        else
        {
            btn.click();
            setTimeout(function(){editortype = _ide.editorManager.getEditorType(); 
                if(editortype === 'cm6')
                {
                    cm6ide = _ide.editorManager.$scope.editor.sharejs_doc.cm6;
                    cm6ide.view.dispatch({changes: { from: cm6ide.shareDoc.getLength(), to: cm6ide.shareDoc.getLength(), insert: data}, selection: {anchor:0}});
                }
                else if(editortype === 'ace')
                    _ide.editorManager.$scope.editor.sharejs_doc.ace.session.replace(new ace.Range(Number.MAX_VALUE, Number.MAX_VALUE, Number.MAX_VALUE, Number.MAX_VALUE), data);
                setTimeout(function(){prebtn.click();
                    setTimeout(function(){
                        if(editortype === 'ace')
                            placebibIds(id, cursor)
                        else if(editortype === 'cm6')
                        {
                            cm6ide = _ide.editorManager.$scope.editor.sharejs_doc.cm6;
                            text = cm6ide.getValue().slice(cm6_f, cm6_t).trim();
                            cm6ide.view.dispatch({changes: { from: cm6_f, to: cm6_t, insert: text+' \\cite{' + id + '}'}, selection: {anchor:0}}) ;
                        }
                            Done.disabled = false;
                            /*Copied.disabled = false;*/}, 
                        1500)}
                ,3000)}
            , 3000);
        }
    }


    function placebibIds(id, cursor)
    {
        x = cursor['row'];
        y = cursor['column'];
        replacer = _ide.editorManager.$scope.editor.sharejs_doc.ace.session;
        replacer.replace(new ace.Range(x,y,x,y), " \\cite{"+id+"}");
    }

    function knowAnchorCursor(){
        anchor = _ide.editorManager.$scope.editor.sharejs_doc.ace.session.getSelection().anchor;
        cursor = _ide.editorManager.$scope.editor.sharejs_doc.ace.session.getSelection().cursor;
        if (anchor['row'] > cursor['row']){
            cursor = anchor;
        }
        else if (anchor['row'] === cursor['row'] && anchor['column'] > cursor['column']){
            cursor = anchor;
        }
        return cursor;
    }


    /*================================================================================*/
    /* -------------------------File: client.js---------------------------------------*/
    /*================================================================================*/
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
        fetch('https://13.233.129.4/cgi-bin/server2.py'+message)
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

}