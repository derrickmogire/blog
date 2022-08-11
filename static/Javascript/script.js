$(document).on('click', '#like', function(event){
    event.preventDefault();
    var pk = $(this).attr('value');
    $.ajax({
      type: 'POST',
      url: '/likes/',
      
      data: {'id':$('#like').attr('value'), 'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()},
      dataType: 'json',
      success: function(){
        
        console.log("success");
      },
      error: function(rs, e){
        console.log(rs.responseText);
      },
    });
  });
 