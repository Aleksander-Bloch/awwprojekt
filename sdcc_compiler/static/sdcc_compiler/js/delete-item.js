const closeDeleteModalBtn = document.querySelector('#close-delete-modal-btn');
deleteAnchor.addEventListener('click', (e) => {
    e.preventDefault();
    fetch(deleteAnchor.href, {
        method: 'GET',
    })
        .then((response) => response.json())
        .then((data) => {
            if (deleteAnchor.href.includes('directory')) {
                const dirItem = document.querySelector(
                    `span.dir-item[data-id="${data['deleted_dir_id']}"]`
                );
                dirItem.parentElement.parentElement.remove();
            } else {
                const fileItem = document.querySelector(
                    `span.file-item[data-id="${data['deleted_file_id']}"]`
                );
                fileItem.parentElement.parentElement.remove();
            }
            selectedItem = selectedItemId = selectedItemName = null;
            closeDeleteModalBtn.click();
        })
        .catch((error) => {
            console.error('Error:', error);
        });

});