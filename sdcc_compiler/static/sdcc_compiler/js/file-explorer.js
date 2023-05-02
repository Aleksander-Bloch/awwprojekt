$(document).ready(function () {
    $('.toggle-collapse').click(function () {
        $(this).find('i').toggleClass('fa-folder fa-folder-open');
        $(this).parent().children('ul').collapse('toggle');
        return false;
    });
});