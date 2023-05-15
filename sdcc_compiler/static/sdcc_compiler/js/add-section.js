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
        })
        .catch((error) => {
            console.error('Error:', error);
        });
});