let selectedItem = null;
let selectedItemId = null;
let selectedItemName = null;
let items = document.querySelectorAll('.dir-item, .file-item');
items.forEach((item) => {
    item.addEventListener('click', () => {
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
    });
});

const addDirModalTrigger = document.querySelector('#add-dir-modal-trigger');
const parentDirInfo = document.querySelector('#parent-dir-info');
const parentInput = document.querySelector('#add-dir-form #id_parent');
const addDirSubmitBtn = document.querySelector('#add-dir-submit-btn');
addDirModalTrigger.addEventListener('click', () => {
    addDirSubmitBtn.disabled = false;
    parentDirInfo.classList.remove('text-danger');
    if (selectedItem === null) {
        parentDirInfo.innerText = "Creating root directory.";
        parentInput.value = null;
    } else if (selectedItem.classList.contains('dir-item')) {
        parentDirInfo.innerText = `Creating directory inside ${selectedItemName}.`;
        parentInput.value = selectedItemId;
        console.log(parentInput.value);
    } else {
        parentDirInfo.innerText = `Please select a parent directory by clicking on a directory item.`;
        addDirSubmitBtn.disabled = true;
        parentDirInfo.classList.add('text-danger');
    }
});