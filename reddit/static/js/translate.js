function simplifyTranslate(event){
    event.preventDefault();
    var $form = $('form');

    $.ajax({
        type: "POST",
        url: "/todos/api/translate/",
        data: $form.serialize(),
        success: function(data) {
            var simplified_temp = "";
            $('#simplified').empty();
            $.each( data.simplified, function( key, value ) {
                simplified_temp += "<p>"+ value + "</p>";
            });
            $('#simplified').append(simplified_temp);

            var translated_temp = "";
            $('#translated').empty();
            $.each( data.translated, function( key, value ) {
                translated_temp += "<p>"+ value + "</p>";
            });
            $('#translated').append(translated_temp);
        },
        error: function (error) {
            console.log(error)
        }
    });
}


