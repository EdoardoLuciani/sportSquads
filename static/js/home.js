$(document).ready(function() {

    var elem_count = 10;
    var end_reached = false;
    async function home_get_10_more_sports() {
        if (end_reached == false) {
            $.ajax({
                url: '/home_get_10_more_sports/' + elem_count,
                type: 'GET',
                dataType: 'json',
                success: function(data) {
                    sports_data = data["sports"]
                    for (var i = 0; i < sports_data.length; i++) {
                        $('#grid-container').append('<div class="sport"> <a href="/sports/' + sports_data[i].name_slug + '">' + sports_data[i].name + '</a> </div>');
                    }
                    elem_count += sports_data.length;
    
                    if (sports_data.length < 10) {
                        end_reached = true;
                    }
                }
            });
        }
    }

    function is_scrollbar_at_end() {
        var scrollerEndPoint = $("#box").prop('scrollHeight') - $("#box").height();
        var divScrollerTop =  $("#box").scrollTop();
        return (scrollerEndPoint - divScrollerTop < 100);
    }

    async function determine_scroll_end() {
        while (is_scrollbar_at_end()) {
            console.log("scroll end");
            home_get_10_more_sports();
            await new Promise(r => setTimeout(r, 1000));
        }
    }

    $('#box').ready(determine_scroll_end);
    $('#box').scroll(determine_scroll_end);
});