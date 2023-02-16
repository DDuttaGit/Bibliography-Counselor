function injectNativeModal(Query) //_ide.showGenericMessageModal('Hii','Bye')
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
                        notifyMe('Bibs have been pasted');
                        /*Copied.disabled = false;*/}, 
                        // cm = _ide.editorManager.$scope.editor.sharejs_doc.cm
                        //  cm.replaceSelection('HI')
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

function notifyMe(msg) {
    if (!("Notification" in window)) {
      alert("This browser does not support desktop notification");
    } else if (Notification.permission === "granted") {
      const notification = new Notification("Hi there!",{
        body: msg,
        vibrate: [200, 100, 200]});
    } else if (Notification.permission !== "denied") {
      Notification.requestPermission().then((permission) => {
        if (permission === "granted") {
          const notification = new Notification("Hi there!",{
                    body: msg,
                    vibrate: [200, 100, 200]});
        }
      });
    }
  }
