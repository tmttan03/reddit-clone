function addItem(event){
    event.preventDefault();
    var $form = $('form');

    $.ajax({
        type: "POST",
        url: "/api/todos/",
        data: $form.serialize(),
        success: function(data) {
            var template = "<p>" +
                "<input type='checkbox'"+
                "id='todo-"+ data.id  +"'" +
                "name='todo-"+ data.id +"'" +
                "value='"+ data.title +"' onchange='updateStatus(event,"+ data.id +", '"+ data.title +"')'> "+
                data.title + "</p>";
            $('#todo-list-body').append(template)
        },
        error: function (error) {
            console.log(error)
        }
    });
}

function resetForm(event){
    event.preventDefault();
    document.getElementById("listForm").reset();
}

function updateStatus(event, id, title){
    event.preventDefault();
    var checkbox = event.target;
    var data = {
        'id': id,
        'title': title,
        'status': false,
        'csrfmiddlewaretoken': $('[name="csrfmiddlewaretoken"]').val()
    }
    if (checkbox.checked) {
        data['status'] = true
    } else {
        data['status'] = false
    }

    $.ajax({
        type: "PUT",
        url: "/api/todos/",
        data: data,
        beforeSend: function (xhr){
            xhr.setRequestHeader('X-CSRFToken', $('input[name=csrfmiddlewaretoken]').val());
        },
        success: function(data) {
            console.log(data);
        },
        error: function (error) {
            console.log(error)
        }
    });
}