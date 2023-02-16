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
