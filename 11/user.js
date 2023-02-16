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
