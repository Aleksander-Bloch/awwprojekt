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

function prepareModal(info, input, submit, target_str) {
    submit.disabled = false;
    info.classList.remove('text-danger');
    if (selectedItem === null) {
        info.innerText = `Creating root ${target_str}.`;
        input.value = null;
    } else if (selectedItem.classList.contains('dir-item')) {
        info.innerText = `Creating ${target_str} inside ${selectedItemName}.`;
        input.value = selectedItemId;
    } else {
        info.innerText = `Please select a parent directory by clicking on a directory item.`;
        submit.disabled = true;
        info.classList.add('text-danger');
    }
}

const addDirModalTrigger = document.querySelector('#add-dir-modal-trigger');
const parentDirInfo = document.querySelector('#parent-dir-info');
const parentInput = document.querySelector('#add-dir-form #id_parent');
const addDirSubmitBtn = document.querySelector('#add-dir-submit-btn');
addDirModalTrigger.addEventListener('click', () => {
    prepareModal(parentDirInfo, parentInput, addDirSubmitBtn, 'directory');
});

const addFileModalTrigger = document.querySelector('#add-file-modal-trigger');
const fileDirInfo = document.querySelector('#file-dir-info');
const fileDirInput = document.querySelector('#add-file-form #id_directory');
const addFileSubmitBtn = document.querySelector('#add-file-submit-btn');

addFileModalTrigger.addEventListener('click', () => {
    prepareModal(fileDirInfo, fileDirInput, addFileSubmitBtn, 'file');
});