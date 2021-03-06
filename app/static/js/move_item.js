$("#sortable").sortable();
$("#sortable").disableSelection();
$(document).ready(function() {

    countTodos();

    // all done btn
    $("#checkAll").on('click', function(){
        console.log('All Done');
        AllDone();
    });

    //create todo
    $('.add-todo').on('keypress',function (e) {
          e.preventDefault
          if (e.which == 13) {
               if($(this).val() != ''){
               var todo = $(this).val();
                createTodo(todo); 
                countTodos();
               } else{
                   // some validation
               }
          }
    });
    // mark task as done
    $('.todolist').on('change','#sortable li input[type="checkbox"]',function(){
        if($(this).prop('checked')){
            var doneItem = $(this).parent().parent().find('label').text();
            $(this).parent().parent().parent().addClass('remove');
            done(doneItem);
            countTodos();
        }
    });

    //delete done task from "already done"
    $('.todolist').on('click','.remove-item',function(){
        console.log('clicked!!!'); 

        removeItem(this);
          if ($('#undotask').on('click')) {
            var timestamp = $('.undotask').html();
            $.ajax({
                url: '/undo',
                type: 'POST',
                data: JSON.stringify({
                    "timestamp": timestamp  
                }, null, '\t'),
                contentType: 'application/json;charset=UTF-8',
                success: function(result) {
                    console.log(result);
                    window.location.reload();
                }
            });
        }
    });

       $('input[type=checkbox]').change(function(){
        // var timestamp = $('#todoTime').text
        if ($('#todoCheck').is(':checked')) {
            var timestamp = $('.todoTime').html();
            $.ajax({
                url: '/donetodos',
                type: 'POST',
                data: JSON.stringify({
                    "timestamp": timestamp  
                }, null, '\t'),
                contentType: 'application/json;charset=UTF-8',
                success: function(result) {
                    console.log(result);
                    window.location.reload();
                }
            })
           // console.log('timestamp: ', $('#todoTime').text());      
        }
    });

    // count tasks
    function countTodos(){
        var count = $("#sortable li").length;
        $('.count-todos').html(count);
    }

    //create task
    function createTodo(text){
        var markup = '<li class="ui-state-default"><div class="checkbox"><label><input type="checkbox" value="" />'+ text +'</label></div></li>';
        $('#sortable').append(markup);
        $('.add-todo').val('');
    }

    //mark task as done
    function done(doneItem){
        var done = doneItem;
        var markup = '<li>'+ done +'<button class="btn btn-default btn-xs pull-right  remove-item"><span class="glyphicon glyphicon-remove"></span></button></li>';
        $('#done-items').append(markup);
        $('.remove').remove();
    }

    //mark all tasks as done
    function AllDone(){
        var myArray = [];

        $('#sortable li').each( function() {
             myArray.push($(this).text());   
        });
        
        // add to done
        for (i = 0; i < myArray.length; i++) {
            $('#done-items').append('<li>' + myArray[i] + '<button class="btn btn-default btn-xs pull-right  remove-item"><span class="glyphicon glyphicon-remove"></span></button></li>');
        }
        
        // myArray
        $('#sortable li').remove();
        countTodos();
    }

    //remove done task from list
    function removeItem(element){
        $(element).parent().remove();
    }
});