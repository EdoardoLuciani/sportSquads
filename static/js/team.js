//$(document).ready(function() { 

//dict(role,quantity){
//   this.role = role;
//   this.quantity = quantity;
// }




// var elem = document.getElementById("roles");
// var roles = document 
// for (var i=0; i<dict.length-1; i++){
//   var dict = new Object();
//   point.role = role;
//   point.quantity = value;

// }



// var i = 0;
// function move() {
//   if (i == 0) {
//     i = 1;
//     var elem = document.getElementById("myBar");
//     var width = 100/dict.role.quantity;
//     var id = setInterval(frame, 10);
//     function frame() {
//       if (width >= 100) {
//         clearInterval(id);
//         i = 0;
//       } else {
//         width++;
//         elem.style.width = width + "%";
//       }
//     }
//   }
// }


// sport_data = data["sport"];
// teams_data = data["teams"];
// document.write("test");
// for (var i = 0; i < sport_data.length; i++) {
//   ('<div id="sport"> <a href="/sport/' + sport_data.name_slug + '">' + sport_data.roles + '</a> </div>');
//   for (var j = 0; j < sports_data.roles.length; i++) {
//     for (var k = 0; k < sports_data.roles[j]; i++) {
//       var elem = document.getElementById("myBar");
//       var width = 100/sports_data.roles[j][k];
//       var id = setInterval(frame, 10);
//       function frame() {
//       if (width >= 100) {
//         clearInterval(id);
//         i = 0;
//       } else {
//         width++;
//         elem.style.width = width + "%";
//         }
//       }

//       for (var i = 0; i < teams_data.length; i++) {
//         for (var i = 0; i < teas_data.members_with_roles.length; i++){
//           if (teas_data.members_with_roles[i][1] == sports_data.roles[j]){
//             frame();
//           }
//         }

//       }
//     }
//   }
// }

//}


// $(document).ready(function(){}

// var counter = 0;
// for (role in sports.roles.items){
//   for (member in  teams.members_with_roles){
//     if (member.role == role){
//       counter = counter +1 ;
//     }
//   }
// }
// document.getElementById('output').innerHTML = counter;




// var elem = document.getElementById("a");

// var tot_val =  {{sports.roles.value}} - {{ teams.members_with_roles[role]}}
// var current_val = 0

// doc.append(<progress id="file" max=tot_val value=current_val> 70% </progress>);


$(document).ready(function() {
    console.log("hello")
    var name = JSON.parse("{{ sport.name|escapejs }}");
    console.log(name)
var interval = 0;
 var tot_val =  "{{sports.roles.value}}" - "{{ teams.members_with_roles[role] }}";
var interval = $('#pagejs_general_delete_wizardresultid').attr('data');;
console.log(JSON.stringify(data))
var progression = 0,
    progress = setInterval(function() 
    {
        $('#progress .progress-text').text(progression + '%');
        $('#progress .progress-bar').css({'width':progression+'%'});
        if(progression == 100) {
            clearInterval(progress);
            alert('done');
        } else
            progression += 10;

    }, 1000);
});

