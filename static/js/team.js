$(document).ready(function() {
    team_json_available_roles = JSON.parse(team_json_available_roles.replace(/'/g, '"'));
    sport_json_roles = JSON.parse(sport_json_roles.replace(/'/g, '"'));

    for (var key in team_json_available_roles) {
        var progress = ((sport_json_roles[key] - team_json_available_roles[key])/parseFloat(sport_json_roles[key]))*100;
        $('#' + key + '-bar').attr('value', progress);
        $('#' + key + '-bar').text(progress + '%');

        $('#' + key + '-label').text(progress + '%');
    }
});

