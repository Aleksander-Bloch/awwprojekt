let selectedItem = null;
let selectedItemId = null;
let selectedItemName = null;
const items = document.querySelectorAll('.dir-item, .file-item');
const fileExplorer = document.querySelector('#file-explorer');


function selectItem(item) {
  if (selectedItem !== null) {
    selectedItem.classList.remove('selected-item');
  }
  if (item === selectedItem) {
    selectedItem = selectedItemId = selectedItemName = null;
    return;
  }
  item.classList.add('selected-item');
  selectedItem = item;
  selectedItemId = item.dataset.id;
  selectedItemName = item.innerText;
  console.log(selectedItemId);
}

items.forEach((item) => {
    item.addEventListener('click', () => {
      selectItem(item);
    });
});


document.querySelectorAll('.file-item').forEach((file) => {
  file.addEventListener('dblclick', function() {
    const file_id = file.dataset.id;
    window.location.href = '/sdcc_compiler/view_file/' + file_id;
  });
});
