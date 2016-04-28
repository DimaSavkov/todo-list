$(document).ready(function (){
    $('#create_form').hide();

    // Hide task form
    $(document).on('click','#create_btn_cancel',function(){
        $('#create_form').hide();
        $('#create_btn_show').show();
        return false
    });

    // show task form
    $(document).on('click','#create_btn_show',function(){
        $('#create_form').show();
        $('#create_btn_show').hide();
        $('#task-text').focus();
        return false
    });

    // send task form to server
    $(document).on('click','#create_btn_save',function(){
        var data = { 'task_text': $('#task-text').val() };
        $.ajax({
            type: "POST",
            url: '/create',
            dataType: "json",
            data: data,
            async: true,
            success: function( data ) {
                var task_li =  '<li class="list-group-item clearfix">' +
                               '<span data-url="/update?id=' + data['id'] + '" class="btn_done state-icon glyphicon glyphicon-unchecked "></span> ' + data['task-text'] +
                               '<span class="pull-right button-group">' +
                               '<a class="btn_delete" data-url="/delete?id=' + data['id'] + '" ><span class="glyphicon glyphicon-trash"></span></a></span></li>';
                $('#todo-list').find('li:last').after(task_li);
                $('#create_form').hide();
                $('#create_btn_show').show();
                $('#task-text').val("");
            },
            error: function (xhr, ajaxOptions, thrownError) {
                 console.log(xhr.status);
                 console.log(thrownError);
            }
        });
        return false
    });

    // delete task
    $(document).on('click','.btn_delete',function(){
        var task_li = $(this).parent().parent();
        $.ajax({
            type: "GET",
            url: $(this).data('url'),
            dataType: "json",
            data: {},
            async: true,
            success: function( data ) {
                task_li.fadeOut(duration=300);
            },
            error: function (xhr, ajaxOptions, thrownError) {
                 console.log(xhr.status);
                 console.log(thrownError);
            }
        });
        return false
    });

    // update task
    $(document).on('click','.btn_done',function(){
        var checkbox = $(this);
        $.ajax({
            type: "GET",
            url: $(this).data('url'),
            dataType: "json",
            data: {},
            async: true,
            success: function( data ) {
                if (checkbox.hasClass('glyphicon-check')){
                    checkbox.removeClass('glyphicon-check').addClass('glyphicon-unchecked');
                    checkbox.parent().removeClass('list-group-item-warning');
                } else {
                    checkbox.removeClass('glyphicon-unchecked').addClass('glyphicon-check');
                    checkbox.parent().addClass('list-group-item-warning');
                }

            },
            error: function (xhr, ajaxOptions, thrownError) {
                 console.log(xhr.status);
                 console.log(thrownError);
            }
        });
        return false
    });

});
