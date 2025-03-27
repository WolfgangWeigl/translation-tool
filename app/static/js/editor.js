// Stelle sicher, dass das DOM geladen ist, bevor der Code ausgeführt wird
document.addEventListener('DOMContentLoaded', function() {
    // Variable für den Diff-Editor
    let diffEditor;

    // Funktion, um den Diff-Editor zu erstellen oder zu aktualisieren
    function updateDiffEditor(tempData) {
        require.config({ paths: { vs: 'https://cdn.jsdelivr.net/npm/monaco-editor@0.51.0/min/vs' } });
        require(['vs/editor/editor.main'], function () {
            if (diffEditor) {
                // Wenn der Editor bereits existiert, aktualisieren wir nur die Modelle
                diffEditor.getModel().original.setValue(tempData.original);
                diffEditor.getModel().modified.setValue(tempData.translation);
            } else {
                // Falls der Editor noch nicht existiert, erstellen wir ihn neu
                diffEditor = monaco.editor.createDiffEditor(document.getElementById('editor'));
                diffEditor.setModel({
                    original: monaco.editor.createModel(tempData.original, 'xml'),
                    modified: monaco.editor.createModel(tempData.translation, 'xml'),
                });
            }
        });
    }

    // Beim Klick auf den "Reset"-Button die Daten neu laden und den Editor zurücksetzen
    document.getElementById('resetBtn').addEventListener('click', function () {
        fetch('/get_diff_data')
            .then(response => response.json())
            .then(tempData => {
                // Diff-Editor mit den neuen Daten aktualisieren
                updateDiffEditor(tempData);
            })
            .catch(error => {
                console.error("Error loading diff data:", error);
            });
    });

    // Initiales Laden der Diff-Daten, wenn die Seite geladen wird
    fetch('/get_diff_data')
        .then(response => response.json())
        .then(tempData => {
            // Initial den Diff-Editor mit den Daten befüllen
            updateDiffEditor(tempData);
        })
        .catch(error => {
            console.error("Error loading diff data:", error);
        });
});
