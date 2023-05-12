const addDirForm = document.querySelector('#add-dir-form');
const fileExplorer = document.querySelector('#file-explorer');
const closeAddDirModalBtn = document.querySelector('#close-add-dir-modal-btn');
addDirForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const formData = new FormData(addDirForm);
    const parentId = formData.get('parent');
    const name = formData.get('name');
    const url = addDirForm.action;
    fetch(url, {
        method: 'POST',
        body: formData,
    })
        .then((response) => response.json())
        .then((data) => {
            console.log('Success:', data);
            const newDir = $(
                `<ul class="list-group">
                    <li class="list-group-item">
                        <span class="dir-item" data-id="${data['directory_id']}">
                            <i class="far fa-folder"></i>${name}
                        </span>
                    </li>
                </ul>`
            );
            const parentSpan = document.querySelector(`span.dir-item[data-id="${parentId}"]`);
            if (parentSpan !== null) {
                $(parentSpan).parent().append(newDir);
            } else {
                $(fileExplorer).append(newDir); // root directory
            }
            closeAddDirModalBtn.click();
        })
        .catch((error) => {
            console.error('Error:', error);
        });
});