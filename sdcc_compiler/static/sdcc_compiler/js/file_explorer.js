document.querySelectorAll('.file-item').forEach((file) => {
  file.addEventListener('dblclick', function() {
    const file_id = file.dataset.id;
    window.location.href = '/sdcc_compiler/view_file/' + file_id;
  });
});
