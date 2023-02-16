PerformDOMOperation();

function PerformDOMOperation()
{
    showPopUp();
    Query = queryExtractor();
    if (Query !== ''){
        getChoiceModal(Query);
    }
    else
        injectNativeModalNoCite();
}


function showPopUp() {
    try{
        var cookie = $.cookie('Counselor_Cookie');
        if(!cookie){
            _ide.showGenericMessageModal('Welcome to Bibliography Counselor', `<u>We will refer <a href="https://sharelatex-wiki-cdn-671420.c.cdn77.org/learn-scripts/images/a/a8/Grammarly1.png" target='_blank'>this image</a> to demonstarte the Query selection process</u><br><br><strong>NO matter which editor you are in, except Rich Text Mode; Just select the text in usual way and press <tt>Ctrl</tt> + <tt>Shift</tt> + <tt>S</tt> for Chrome and <tt>Ctrl</tt> + <tt>Shift</tt> + <tt>U</tt> for Firefox; More info is in <a href="https://13.233.129.4/homepage.html" target="_blank">here</strong>`);
            $.cookie('Counselor_Cookie', '0');
        }
    }
    catch(e)
    {
        alert("Please open a Project first")
    }
}