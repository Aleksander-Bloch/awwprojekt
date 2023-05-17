const downloadBtn = document.getElementById('download-btn');

downloadBtn.addEventListener('click', (e) => {
    const asmSections = localStorage.getItem('asm_sections');
    if (asmSections === null) {
        e.preventDefault()
        alert('Only files that have been successfully compiled can be downloaded.');
    }
});