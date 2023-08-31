
$("#new-car").on('click', function(e){
    $('#car-form').css('display', 'block');
    $('#new-car-header').css('display', 'block');
    $(this).css('display', 'none');
})


$(document).on('click','a#delete-car',(function(e){    
    thisId = $(this).data('id')
    e.preventDefault();    
    $.post('delete_car/',      
        {id: $(this).data('id')},     
        function(data){     
            if (data['status'] == 'ok'){
                $('div#car-'+thisId).remove()
            }   
            else{
                $('#content').append(
                    `<br class="space"/>
                    <br class="space"/>
                    <ul class="error">
                        <li class="errorlist"> You can't delete this car because you have orders for this car <i class="far fa-times-circle"></i></li>
                    </ul>
                    <br class="space"/>`
                )
            }
        });  
    })); 

    $(document).on('change','#id_date_day',(function(e){    
        e.preventDefault();    
        $.post('appointment',      
            {month: $('#id_date_month').val(), day:$('#id_date_day').val(), chosing: true},     
            function(data){     
                if (data['status'] == 'ok'){
                   $('#time-select>option').remove();
                   data['times'].forEach(element => {
                       $('#time-select').append(`<option value="${element}">${element}</option>`)
                   });
                }   
            });  
        })); 

$(document).on('click','i.far',(function(e){   
    $('ul.error').remove();
    $('br.space').remove();
}))


$('#car-form').submit(function(e){
    e.preventDefault();
    let frm = $('#car-form')
    $.post('/account/',
        {
            make: $('#id_make').val(),
            model: $('#id_model').val(),
            year: $('#id_year').val(),
            vin: $('#id_vin').val()
        },
        function(data){
            if (data['status'] == 'ok'){
                $('.all-cars').append(
                    `<div class="car" id="car-${data['car']['id']}">   
                    <!-- <img src="{% static "images/service-2.png" %}" alt=""> -->
                    <i class="fa fa-car"></i>
                    <p>Make:  <span><br/>${data['car']['make']}</span></p>
                    <p>Model: <span><br/>${data['car']['model']}</span></p>
                    <p>Year: <span><br/>${data['car']['year']}</span></p>
                    <p>VIN: <span><br>${data['car']['vin']}</span></p>
                    <a id="delete-car" class="button" data-id="${data['car']['id']}">Delete</a>
                    </div>`
                )
                $('#car-form').css('display', 'none');
                $('#new-car-header').css('display', 'none');
                $('#new-car').css('display', 'block');
            }
        }
)})