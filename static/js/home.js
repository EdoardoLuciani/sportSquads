$(document).ready(function() {

    function scrollbar_at_end() {
        var scrollerEndPoint = $("#box").prop('scrollHeight') - $("#box").height();
        var divScrollerTop =  $("#box").scrollTop();
        return (scrollerEndPoint - divScrollerTop) < 150;
    }

    var elem_count = 10;
    var end_reached = false;
    var request_in_progress = false;
    function home_get_more_sports_while_scroll_end() {
        if (!end_reached && !request_in_progress && scrollbar_at_end()) {
            var request = $.ajax({
                url: '/home_get_10_more_sports/' + elem_count,
                type: 'GET',
                dataType: 'json',
            });
            request_in_progress = true;
            request.done(function(data) {
                sports_data = data["sports"];
                for (var i = 0; i < sports_data.length; i++) {
                    var new_sport = $('.link-box ').last().clone();
                    new_sport.text(sports_data[i].name);
                    new_sport.attr('href', '/sport/' + sports_data[i].name_slug);
                    new_sport.css('background-image', 'url(/media/' + sports_data[i].image +')');

                    $('#grid-container').append(new_sport);
                }
                elem_count += sports_data.length;

                request_in_progress = false;

                if (sports_data.length < 10) {
                    end_reached = true;
                }
                else if (scrollbar_at_end()) {
                    home_get_more_sports_while_scroll_end()
                }
            });
        }
    }

    $('#box').ready(home_get_more_sports_while_scroll_end);
    $('#box').scroll(home_get_more_sports_while_scroll_end);
});
