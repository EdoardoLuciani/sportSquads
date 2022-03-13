$(document).ready(function() {

    function scrollbar_at_end() {
        var scrollerEndPoint = $("#box").prop('scrollHeight') - $("#box").height();
        var divScrollerTop =  $("#box").scrollTop();
        return (scrollerEndPoint - divScrollerTop < 100);
    }


    var slugs = document.URL.split('/');
    var sport_name = slugs[slugs.length - 2]

    var elem_count = 10;
    var end_reached = false;
    var request_in_progress = false;
    function sport_get_more_teams_while_scroll_end() {
        if (!end_reached && !request_in_progress) {
            var request = $.ajax({
                url: '/sport_get_10_more_teams/' + sport_name + "/" + elem_count,
                type: 'GET',
                dataType: 'json',
            });
            request_in_progress = true;
            request.done(function(data) {
                request_in_progress = false;

                teams_data = data["teams"];
                for (var i = 0; i < teams_data.length; i++) {
                    $('#grid-container').append('<div class="team"> <a href="/team/' + teams_data[i].name_slug + '">' + teams_data[i].name + '</a> </div>');
                }
                elem_count += teams_data.length;

                if (teams_data.length < 10) {
                    end_reached = true;
                }
                else if (scrollbar_at_end()) {
                    sport_get_more_teams_while_scroll_end()
                }
            });
        }
    }

    $('#box').ready(sport_get_more_teams_while_scroll_end);
    $('#box').scroll(sport_get_more_teams_while_scroll_end);
});
