function prepareAddModal(info, input, submit, target_str) {
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
    prepareAddModal(parentDirInfo, parentInput, addDirSubmitBtn, 'directory');
});

const addFileModalTrigger = document.querySelector('#add-file-modal-trigger');
const fileDirInfo = document.querySelector('#file-dir-info');
const fileDirInput = document.querySelector('#add-file-form #id_directory');
const addFileSubmitBtn = document.querySelector('#add-file-submit-btn');

addFileModalTrigger.addEventListener('click', () => {
    prepareAddModal(fileDirInfo, fileDirInput, addFileSubmitBtn, 'file');
});

function prepareDeleteModal(info, submitAnchor, submitBtn) {
    submitBtn.disabled = false;
    submitAnchor.style.pointerEvents = 'auto';
    info.classList.remove('text-danger');
    if (selectedItem === null) {
        info.innerText = `Please select file or a directory.`;
        submitBtn.disabled = true;
        submitAnchor.style.pointerEvents = 'none';
        info.classList.add('text-danger');
    } else {
        if (selectedItem.classList.contains('dir-item')) {
            info.innerText = `Are you sure you want to delete directory ${selectedItemName} and all its contents?`;
            submitAnchor.href = `/sdcc_compiler/delete/directory/${selectedItemId}`;
        } else {
            info.innerText = `Are you sure you want to delete file ${selectedItemName}?`;
            submitAnchor.href = `/sdcc_compiler/delete/file/${selectedItemId}`;
        }
    }
}

const deleteModalTrigger = document.querySelector('#delete-modal-trigger');
const deleteInfo = document.querySelector('#delete-info');
const deleteAnchor = document.querySelector('#delete-anchor');
const deleteBtn = document.querySelector('#delete-btn');

deleteModalTrigger.addEventListener('click', () => {
    prepareDeleteModal(deleteInfo, deleteAnchor, deleteBtn);
});

const addSectionModalTrigger = document.querySelector('#add-section-modal-trigger');
const addSectionInfo = document.querySelector('#add-section-info');
const addSectionSubmitBtn = document.querySelector('#add-section-submit-btn');
const startLineInput = document.querySelector('#add-section-form #id_start_line');
const endLineInput = document.querySelector('#add-section-form #id_end_line');
const contentInput = document.querySelector('#add-section-form #id_content');
const fileInput = document.querySelector('#add-section-form #id_file');

addSectionModalTrigger.addEventListener('click', () => {
    addSectionSubmitBtn.disabled = false;
    addSectionInfo.classList.remove('text-danger');

    const selection = window.getSelection();
    const selectedText = selection.toString();
    if (selectedText.length === 0) {
        addSectionInfo.innerText = `Please highlight text in the program viewer.`;
        addSectionSubmitBtn.disabled = true;
        addSectionInfo.classList.add('text-danger');
    } else {
        const selectedRange = selection.getRangeAt(0);
        const startingLine = selectedRange.startContainer.parentElement.dataset.line;
        const endingLine = selectedRange.endContainer.parentElement.dataset.line;
        addSectionInfo.innerText = `Adding section from line ${startingLine} to line ${endingLine}.`;
        startLineInput.value = startingLine;
        endLineInput.value = endingLine;
        contentInput.value = selectedText;
        fileInput.value = editorFileId;
    }
});

const logoutBtn = document.querySelector('#logout-btn');
logoutBtn.addEventListener('click', () => {
    localStorage.clear();
});

const toastTrigger = document.getElementById('liveToastBtn');
const toastLiveInfo = document.getElementById('liveToast');
const toastHeader = toastLiveInfo.querySelector('.toast-header');
const toastBody = toastLiveInfo.querySelector('.toast-body');
const toastSrc = toastLiveInfo.querySelector('#toastSrc');

if (toastTrigger) {
    const toastBootstrap = bootstrap.Toast.getOrCreateInstance(toastLiveInfo, {delay: 3000})
    toastTrigger.addEventListener('click', () => {
        toastBootstrap.show();
    })
}


