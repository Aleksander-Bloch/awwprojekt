const addFileForm = document.querySelector('#add-file-form');
const closeAddFileModalBtn = document.querySelector('#close-add-file-modal-btn');

addFileForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const formData = new FormData(addFileForm);
    const directoryId = formData.get('directory');
    const name = formData.get('name');
    const url = addFileForm.action;
    fetch(url, {
        method: 'POST',
        body: formData,
    })
        .then((response) => response.json())
        .then((data) => {
            const newFile = $(
                `<ul class="list-group">
                    <li class="list-group-item">
                        <span class="file-item" data-id="${data['file_id']}">
                            <i class="far fa-file"></i>${name}
                        </span>
                    </li>
                </ul>`
            );
            const parentSpan = document.querySelector(`span.dir-item[data-id="${directoryId}"]`);
            if (parentSpan !== null) {
                $(parentSpan).parent().append(newFile);
            } else {
                $(fileExplorer).append(newFile); // root directory
            }
            const newFileSpan = newFile.find('span.file-item');
            newFileSpan.click(() => {selectItem(newFileSpan[0])});
            newFileSpan.dblclick(() => {
                const file_id = newFileSpan.data('id');
                window.location.href = '/sdcc_compiler/view_file/' + file_id;
            });
            closeAddFileModalBtn.click();
            addFileForm.reset();
        })
        .catch((error) => {
            console.error('Error:', error);
        });
});