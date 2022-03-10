$(document).ready(function() {
    $('div').scroll(function() {
        var div = $(this);
        if (div.height() == div.scrollTop() + 1) {
            alert('Reached the bottom!");
        }
    });
});