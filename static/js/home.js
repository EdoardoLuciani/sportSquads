$(document).ready(function() {
    $('#box').scroll(function() {
        var scrollerEndPoint = $("#box").prop('scrollHeight') - $("#box").height();

        var divScrollerTop =  $("#box").scrollTop();

        if(scrollerEndPoint - divScrollerTop < 100) {
            alert("Scrolled to the bottom!");
        }
    });
});