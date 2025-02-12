// Socket Handling
const socket = io();

// Handle form submission
document.getElementById('translateBtn').addEventListener('click', function (event) {
  document.getElementById('progress-bars').removeAttribute('hidden');
  const file = document.getElementById('fileinput').files[0];
  socket.emit('upload', {
    fileName: file.name,
    fileType: document.querySelector('[data-type]').getAttribute('data-type'),
    fileData: file,
    srcLang: document.getElementById('originalLanguage').value,
    destLang: document.getElementById('targetLanguage').value
  });
});

// Listen for upload progress
socket.on('upload_progress', (data) => {
  const progressBar = document.getElementById('progress-bar-1');
  progressBar.textContent = `${data.progress.toFixed(2)}%`;
  progressBar.style.width = `${data.progress}%`;
  if (data.finished) progressBar.classList.remove('progress-bar-animated');
});

// Listen for extraction progress
socket.on('extraction_progress', (data) => {
  const progressBar = document.getElementById('progress-bar-2');
  progressBar.textContent = `${data.progress.toFixed(2)}%`;
  progressBar.style.width = `${data.progress}%`;
  if (data.finished) progressBar.classList.remove('progress-bar-animated');
});

// Listen for extraction progress
socket.on('translation_progress', (data) => {
  const progressBar = document.getElementById('progress-bar-3');
  // progressBar.textContent = `${data.progress.toFixed(2)}%`;
  // progressBar.style.width = `${data.progress}%`;
  if (data.finished) {
    progressBar.classList.remove('progress-bar-animated');
    document.getElementById('editorBtn').closest('div').removeAttribute('hidden');
    document.getElementById('downloadBtn').closest('div').removeAttribute('hidden');
  }
});

// Redirection to diff-editor
document.getElementById('editorBtn').addEventListener("click", function () {
  window.location.href = '/editor';
})