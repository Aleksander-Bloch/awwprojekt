let selectedItem = null;
let selectedItemId = null;
let selectedItemName = null;
let editorFileId = localStorage.getItem('editor_file_id');
const items = document.querySelectorAll('.dir-item, .file-item');
const fileExplorer = document.querySelector('#file-explorer');
const programViewer = document.querySelector('#program-viewer');
const sectionList = document.querySelector('#section-list');

function updateCFileSections(sections) {
    sections.forEach((section) => {
        const newSection = $(
            `<li class="list-group-item d-flex justify-content-between align-items-start">
                <div class="ms-2 me-auto">
                    <div class="fw-bold">${section['type']}</div>
                    Lines: ${section['start']} - ${section['end']}
                </div>
                <span class="badge bg-success rounded-pill">${section['status']}</span>
            </li>`
        );
        $(sectionList).append(newSection);
    });
}

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

function createProgramLines(fileContent) {
    const fileContentLines = fileContent.split('\n');
    for (let lineNo = 0; lineNo < fileContentLines.length; lineNo++) {
        const programLine = $(
            `<div class="program-line" data-line="${lineNo + 1}"></div>`
        );
        if (fileContentLines[lineNo] === '') {
            programLine.text('\n');
        } else {
            programLine.text(fileContentLines[lineNo]);
        }
        $(programViewer).append(programLine);
    }
}

function viewFile(file) {
    const file_id = file.dataset.id;
    fetch('/sdcc_compiler/view_file/' + file_id, {
        method: 'GET',
    })
        .then((response) => response.json())
        .then((data) => {
            editorFileId = file_id;
            programViewer.innerHTML = '';
            createProgramLines(data['file_content']);
            sectionList.innerHTML = '';
            updateCFileSections(data['sections']);
            fragmentViewer.innerHTML = '';
            localStorage.removeItem('asm_sections');
            localStorage.removeItem('errors');

            localStorage.setItem('file_content', data['file_content']);
            localStorage.setItem('editor_file_id', file_id);
            localStorage.setItem('sections', JSON.stringify(data['sections']));
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}

const content = localStorage.getItem('file_content');
if (content !== null) {
    createProgramLines(content);
}
const sections = JSON.parse(localStorage.getItem('sections'));
if (sections !== null) {
    updateCFileSections(sections);
}

items.forEach((item) => {
    item.addEventListener('click', () => {
        selectItem(item);
    });
});

document.querySelectorAll('.file-item').forEach((file) => {
    file.addEventListener('dblclick', () => {
        viewFile(file);
    });
});
