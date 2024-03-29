const compilationForm = document.getElementById('compilation-form');
const fragmentViewer = document.getElementById('fragment-viewer');

function updateAsmSections(asmSections) {
    asmSections.forEach((section) => {
        const sectionClass = section['is_header'] ? 'asm-header' : 'asm-body';
        const newSection = $(
            `<div class="${sectionClass}">${section['content']}</div>`
        );
        $(fragmentViewer).append(newSection);
        if (!section['is_header']) {
            const header = newSection[0].previousElementSibling;
            if (header !== null) {
                $(header).click(() => {
                    $(newSection).toggle('smooth');
                });
            }
        }
    });
}

function updateErrors(errors) {
    errors.forEach((error) => {
        const newError = $(
            `<div class="error"></div>`
        );
        newError.text(error['error_message']);
        const lineNo = error['line_number'];
        const programLine = $(`.program-line[data-line="${lineNo}"]`);
        newError.mousedown(() => {
            $(programLine).addClass('error-line');
            programLine[0].scrollIntoView();
        });
        newError.mouseup(() => {
            $(programLine).removeClass('error-line');
        });
        $(fragmentViewer).append(newError);
    });
}

compilationForm.addEventListener('submit', (e) => {
    e.preventDefault();
    if (editorFileId === null) {
        alert('Please double-click on the file to view it in editor before compiling.');
        return;
    }
    const formData = new FormData(compilationForm);
    fetch(`/sdcc_compiler/compile/${editorFileId}/`, {
        method: 'POST',
        body: formData,
    })
        .then((response) => response.json())
        .then((data) => {
            fragmentViewer.innerHTML = '';
            $(toastSrc).text('Compile');
            if ('errors' in data) {
                updateErrors(data['errors']);
                localStorage.setItem('errors', JSON.stringify(data['errors']));
                localStorage.removeItem('asm_sections');
                toastHeader.classList.remove('bg-success');
                toastHeader.classList.remove('bg-primary');
                toastHeader.classList.add('bg-danger');
                $(toastBody).text('Compilation failed');
            }
            else {
                updateAsmSections(data['asm_sections']);
                localStorage.setItem('asm_sections', JSON.stringify(data['asm_sections']));
                localStorage.removeItem('errors');
                toastHeader.classList.remove('bg-danger');
                toastHeader.classList.remove('bg-primary');
                toastHeader.classList.add('bg-success');
                $(toastBody).text('Compilation successful');
            }
            toastTrigger.click();
        })
        .catch((error) => {
            console.error('Error:', error);
        });
});

const asmSections = JSON.parse(localStorage.getItem('asm_sections'));
if (asmSections !== null) {
    updateAsmSections(asmSections);
}
const errors = JSON.parse(localStorage.getItem('errors'));
if (errors !== null) {
    updateErrors(errors);
}