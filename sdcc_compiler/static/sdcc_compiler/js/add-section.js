const addSectionForm = document.querySelector('#add-section-form');
const closeAddSectionModalBtn = document.querySelector('#close-add-section-modal-btn');

addSectionForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const formData = new FormData(addSectionForm);
    fetch(`/sdcc_compiler/add_section/`, {
        method: 'POST',
        body: formData,
    })
        .then((response) => response.json())
        .then((data) => {
            updateCFileSections([data]);
            const sections = JSON.parse(localStorage.getItem('sections'));
            sections.push(data);
            localStorage.setItem('sections', JSON.stringify(sections));
            closeAddSectionModalBtn.click();
            $(toastSrc).text('Add section');
            toastHeader.classList.remove('bg-danger');
            toastHeader.classList.remove('bg-success');
            toastHeader.classList.add('bg-primary');
            $(toastBody).text(`Check out your new section in "Sections/View list".`);
            toastTrigger.click();
        })
        .catch((error) => {
            console.error('Error:', error);
        });
});