function displayTopTen(){
    var request = $.ajax({
        method: 'GET',
        url: '../WordFrequency.json', //todo change url
        dataType: 'json'
    });

    request.done(function (json) {
        console.log(json)  //todo
    });

    request.fail(function( jqXHR, textStatus ) {
        alert( "Request failed: " + textStatus );
    });
}