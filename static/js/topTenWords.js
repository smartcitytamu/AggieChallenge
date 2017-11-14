function displayTopTen(){
    var request = $.ajax({
        method: 'GET',
        url: '0.0.0.0:5000/topTen.json', //todo change url
        dataType: 'json'
    });

    request.done(function (json) {
        console.log(json)  //todo
    });

    request.fail(function( jqXHR, textStatus ) {
        alert( "Request failed: " + textStatus );
    });
}