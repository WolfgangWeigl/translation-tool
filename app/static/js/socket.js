// Socket Handling
const socket = io();

const form = document.getElementById('upload-form')
const allFormInputs = form.querySelectorAll('input, select');
const fileLabel = document.querySelector('label.form-control');

const fileInput = document.getElementById('fileinput');
const originalLanguage = document.getElementById('originalLanguage');
const targetLanguage = document.getElementById('targetLanguage');
const translationType = document.querySelector('input[name="translationType"]:checked');

const translateBtn = document.getElementById('translateBtn');
const editorBtn = document.getElementById('editorBtn');
const downloadBtn = document.getElementById('downloadBtn');
const progressBarContainer = document.getElementById('progress-bars');

// Handle form submission
form.addEventListener('submit', function (event) {
  event.preventDefault();

  if (form.checkValidity()) {
    // Disable all form inputs and adjust styling
    allFormInputs.forEach(e => e.disabled = true);
    fileLabel.classList.add("disabled", "btn-outline-secondary");

    // Update the translate button (change text and disable it)
    translateBtn.innerHTML = '<i class="bi bi-hourglass-split"></i> Translating...';
    translateBtn.disabled = true;

    // Show the progress bars and hide other buttons
    progressBarContainer.removeAttribute('hidden');
    editorBtn.closest('div').setAttribute('hidden', '');
    downloadBtn.closest('div').setAttribute('hidden', '');

    // Reset progress bars and start animation
    document.querySelectorAll('.progress-bar').forEach(bar => {
      bar.textContent = '0%';
      bar.style.width = '0%';
      bar.classList.add('progress-bar-animated');
      bar.classList.remove('bg-success');
    });

    // Upload
    socket.emit('upload', {
      fileName: fileInput.files[0].name,
      fileType: document.querySelector('[data-type]').getAttribute('data-type'),
      fileData: fileInput.files[0],
      srcLang: originalLanguage.value,
      destLang: targetLanguage.value,
      transType: translationType.value
    });
  } else {
    form.reportValidity();
  }
});

// Listen for upload progress
socket.on('upload_progress', (data) => {
  const progressBar = document.getElementById('progress-bar-1');
  progressBar.textContent = `${data.progress.toFixed(2)}%`;
  progressBar.style.width = `${data.progress}%`;
  if (data.finished) {
    progressBar.classList.remove('progress-bar-animated');
    progressBar.classList.add('bg-success');
  }
});

// Listen for extraction progress
socket.on('extraction_progress', (data) => {
  const progressBar = document.getElementById('progress-bar-2');
  progressBar.textContent = `${data.progress.toFixed(2)}%`;
  progressBar.style.width = `${data.progress}%`;
  if (data.finished) {
    progressBar.classList.remove('progress-bar-animated');
    progressBar.classList.add('bg-success');
  }
});

// Listen for extraction progress
socket.on('translation_progress', (data) => {
  const progressBar = document.getElementById('progress-bar-3');
  progressBar.textContent = `${data.progress.toFixed(2)}%`;
  progressBar.style.width = `${data.progress}%`;
  if (data.finished) {
    progressBar.classList.remove('progress-bar-animated');
    progressBar.classList.add('bg-success');
    // Enable form elements and change button text
    allFormInputs.forEach(e => e.disabled = false);
    fileLabel.classList.remove("disabled", "btn-outline-secondary");
    translateBtn.innerHTML = '<i class="bi bi-translate"></i>Translate';
    translateBtn.disabled = false;
    // Display other buttons
    editorBtn.closest('div').removeAttribute('hidden');
    downloadBtn.closest('div').removeAttribute('hidden');
  }
});