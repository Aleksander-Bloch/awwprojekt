$(document).ready(function () {
    let elementsVisible = true;

    $('#toggle-all-sections-btn').click(function () {
        if (elementsVisible) {
            $('.asm-body').hide("smooth");
            elementsVisible = false;
            $(this).text("Show");
        } else {
            $('.asm-body').show("smooth");
            elementsVisible = true;
            $(this).text("Hide");
        }
    });
});

