function displayTopTen(){
    $.ajax({
        method: 'GET',
        url: '0.0.0.0:5000/topTen.json',
        dataType: 'json'
    });
}