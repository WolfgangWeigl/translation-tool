fetch('/get_diff_data')
    .then(response => response.json())
    .then(tempData => {
        require.config({ paths: { vs: 'https://cdn.jsdelivr.net/npm/monaco-editor@0.51.0/min/vs' } });
        require(['vs/editor/editor.main'], function () {
            monaco.editor.createDiffEditor(document.getElementById('editor')).setModel({
                original: monaco.editor.createModel(tempData.original, 'xml'),
                modified: monaco.editor.createModel(tempData.translation, 'xml'),
            })
        });
    });