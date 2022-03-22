$(document).ready(function() { 

    $('#add_new_sport').on('input', 'p:nth-last-of-type(2)', function() {
        if ($(this).find('input').val().length > 0) {
            var idx = parseInt($(this).find('label').text().slice(5).slice(0,-1)) + 1;
    
            var last_elem = $(this).next().after('<p> <label for="id_role_'+ idx +'">Role '+ idx +':</label> <input type="text" name="role_'+ idx +'" maxlength="64" id="id_role_'+ idx +'"> </p>');
            $(last_elem).next().after('<p> <label for="id_role_'+ idx +'_count">Role '+ idx +' count:</label> <input type="number" name="role_'+ idx +'_count" min="1" id="id_role_'+ idx +'_count"> </p>');
            
            var current_height = parseInt($('.input-box').css('height').slice(0, -2));
            $('.input-box').css('height', current_height + 90 + 'px');
        }
    });

});