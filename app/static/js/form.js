// File Selection Modification
document.getElementById('fileinput').addEventListener('change', e => {
    document.getElementById('filename').textContent = e.target.files[0]?.name || 'No file selected';
  });


// Target Language disabled if no Original Language is selected
document.getElementById("originalLanguage").addEventListener("change", function () {
    let target = document.getElementById("targetLanguage");
    if (this.value !== "") {
        target.disabled = false;
    } else {
        target.disabled = true;
    }
});


// Available Target Languages based on selected Source Language
document.getElementById('originalLanguage').addEventListener('change', function () {

    const langs = JSON.parse(document.querySelector('[data-langs]').getAttribute('data-langs'));
  
    const srcLang = this.value;
    const destLang = document.getElementById('targetLanguage');
    destLang.innerHTML = "<option value='' disabled selected>---</option>"
  
    const language = langs.find(l => l.code === srcLang);
  
    if (language) {
      language.targets.forEach(target => {
        if (target !== srcLang) {
          const option = document.createElement('option');
          option.value = target;
          option.textContent = langs.find(l => l.code === target).name;
          destLang.appendChild(option);
        }
      });
    }
  });
