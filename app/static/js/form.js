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
      const sortedTargets = language.targets
      .filter(target => target !== srcLang) 
      .map(target => ({
          code: target,
          name: langs.find(l => l.code === target).name
      }))
      .sort((a, b) => a.name.localeCompare(b.name)); 

      sortedTargets.forEach(target => {
          const option = document.createElement('option');
          option.value = target.code;
          option.textContent = target.name;
          destLang.appendChild(option);
      });
    }
  });

  // // Set default value after a refresh
  // window.onload = function() {
  //   // document.getElementById('originalLanguage').value = ''; 
  //   // document.getElementById('targetLanguage').value = ''; 
  //   document.getElementById('upload-form').reset();
  // }
  
  // Demo Mode
  document.addEventListener('DOMContentLoaded', function () {
    const isDemo = document.querySelector('[data-demo]')?.getAttribute('data-demo') === 'True';

    if (isDemo) {
      const fileInput = document.getElementById('fileinput');
      const fileName = document.getElementById('filename');
      const originalLanguage = document.getElementById('originalLanguage');
      const targetLanguage = document.getElementById('targetLanguage');

      const blob = new Blob(["<root></root>"], { type: "DEMO" });
      const demoFile = new File([blob], 'demo.xml', { type: 'DEMO' });
      const dt = new DataTransfer();
      dt.items.add(demoFile);
      fileInput.files = dt.files;
      fileName.textContent = demoFile.name;

      originalLanguage.value = 'de';
      originalLanguage.dispatchEvent(new Event('change'));
      targetLanguage.value = 'en';
    }




  });