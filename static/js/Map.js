var map;
var user_location;

var connect_id;
var points = [];
var run = true;

var bounds;
var icons;


function initMap() {
  map = new google.maps.Map(document.getElementById('map'), {
    center: {lat: 30.272, lng: -97.742},
    zoom: 13
  });
  icons = [{
            path: google.maps.SymbolPath.CIRCLE,
            scale: 4,
            strokeColor: "Grey"
          },
          {
            path: google.maps.SymbolPath.BACKWARD_CLOSED_ARROW,
            scale: 4,
            strokeColor: "Grey"
          },
          {
            path: google.maps.SymbolPath.CIRCLE,
            scale: 4,
            strokeColor: "Green"
          },
          {
            path: google.maps.SymbolPath.BACKWARD_CLOSED_ARROW,
            scale: 4,
            strokeColor: "Green"
          }
  ];
  getUserLocation();
  connectToTweet();
}

function connectToTweet(){
   var client = new XMLHttpRequest();
   bounds = getBoundingBox(map);

   console.log(bounds);

   NElat = bounds.getNorthEast().lat();
   NElng = bounds.getNorthEast().lng();
   SWlat = bounds.getSouthWest().lat();
   SWlng = bounds.getSouthWest().lng();

   open_url = '../openTweetConnection.js?'+'NElat='+NElat+'&NElng='+NElng+'&SWlat='+SWlat+'&SWlng='+SWlng;
   client.open('GET', open_url);
   client.responseType = "json";

   client.onreadystatechange = function() {
     if(client.readyState === XMLHttpRequest.DONE && client.status === 200) {
           console.log('connected');
           //setInterval(updateTweets(map.getBounds()), 1000);
           updateTweets(map.getBounds());
     }
   }
   client.send();
}

function updateTweets(){
   var client = new XMLHttpRequest();

   tweets_url = '../tweets.json';
   client.open('GET', tweets_url);
   client.responseType = "json";

   client.onreadystatechange = function() {
     if(client.readyState === XMLHttpRequest.DONE && client.status === 200) {
         tweets = client.response;
         console.log("Tweets: " + tweets);
         tweets.forEach(function(tweet, index){
            //add tweets to map
            addTweet(tweet);
            console.log("Tweet: " + tweet);
         });
         if(!user_location != null){
            user_location.setZIndex(google.maps.Marker.MAX_ZINDEX + 1);
         }
     }
   }
   client.send();

   //setTimeout(updateTweets(map.getBounds()), 2500);
}

// Convert Tweet json into Map Marker
function addTweet(tweet){
    exact = false;
    myIcon = icons[0];
    //is a location provided?
    if(tweet.geo != null){
      latitude = tweet.geo.coordinates[0];
      longitude = tweet.geo.coordinates[1];
      //change icon to show it's an exact location
      exact = true;
      myIcon = icons[1];
    } else {
        bounding_box = tweet.place.bounding_box.coordinates;
        lat_distance = Math.abs(bounding_box[0][0][1] - bounding_box[0][2][1]);
        lng_distance = Math.abs(bounding_box[0][0][0] - bounding_box[0][2][0]);

        console.log(bounding_box);
        console.log("LatDist: " + lat_distance);
        console.log("LngDist: " + lng_distance);

        latitude = bounding_box[0][0][1] + lat_distance * Math.random();
        longitude = bounding_box[0][0][0] + lng_distance * Math.random();

        console.log("Lat: " + latitude);
        console.log("Lng: " + longitude);
    }

    if(tweet.text == null)
        tweet.text = "NO TEXT";

   addTweetToList(tweet);

   marker = new google.maps.Marker({
    id: tweet.id,
    user_id: tweet.user.id,
    position: {lat: latitude, lng: longitude},
    text: tweet.text,
    map: map,
    exact: exact,
    infowindow: new google.maps.InfoWindow({
          content: contentString
    }),
    icon: myIcon
  });

  marker.addListener('click', function(e){
    //scroll to tweet
    $('#tweets-list').animate({
       scrollTop: $('#tweets-list > #' + tweet.id).position().top - $('#tweets-list li:first').position().top
    }, 'slow');

    this.infowindow.open(map, this);
  });

  points.push(marker);
}

function addTweetToList(tweet){
    //create content string for displaying info about tweet
    contentString = '<div id="content" style="width: 233px">'+
             '<h3 id="firstHeading" class="firstHeading">' + tweet.user.name + '</h3>'+
             'Followers: ' + tweet.user.followers_count +
             '<div id="bodyContent">'+
              tweet.text + '<br/>' +
             '</div>'+
             '</div>';

    $('#tweets-list').append("<li id=" + tweet.id + " class='list-group-item'>" + contentString + "</li>")
}

function search(terms){
    terms = terms.replace(/ /g, '')
    terms_array = terms.split(',')
    console.log(terms_array);
    points.forEach(function(point, index){
        changeTweetToGrey(point);
        terms_array.forEach(function(term, index){
             if(point.text.includes(term)){
                console.log(point.text);
                changeTweetToGreen(point);
             }
        });
    });
}

function changeTweetToGreen(marker){
    if(marker.exact){
        marker.setIcon(icons[3]);
    }else{
        marker.setIcon(icons[2]);
    }
}

function changeTweetToGrey(marker){
    if(marker.exact){
        marker.setIcon(icons[1]);
    }else{
        marker.setIcon(icons[0]);
    }
}

function getBoundingBox(map){
    bounds = map.getBounds();
    if(bounds == undefined){
        //better box from center and zoom
        bounds = new google.maps.LatLngBounds(new google.maps.LatLng(map.center.lat()-0.2, map.center.lng()-0.2),
                                              new google.maps.LatLng(map.center.lat()+0.2, map.center.lng()+0.2));
    }
    return bounds;
}

function getUserLocation(){
   window.alert("User Location");
   if (navigator.geolocation) {
     navigator.geolocation.getCurrentPosition(function(position) {
       var pos = {
         lat: position.coords.latitude,
         lng: position.coords.longitude
       };

       user_location = new google.maps.Marker({
          position: pos,
          map: map,
          icon: { path: google.maps.SymbolPath.CIRCLE,
                  scale: 5,
                  fillColor: "Blue",
                  fillOpacity: 0.6,
                  strokeColor: "White",
                  strokeWeight: 1,
                }
       });

       map.setCenter(pos);
     }, function() {
       handleLocationError(true, infoWindow, map.getCenter());
     });
   } else {
     // Browser doesn't support Geolocation
     handleLocationError(false, infoWindow, map.getCenter());
   }
}

function handleLocationError(browserHasGeolocation, infoWindow, pos) {
   infoWindow.setPosition(pos);
   infoWindow.setContent(browserHasGeolocation ?
                         'Error: The Geolocation service failed.' :
                         'Error: Your browser doesn\'t support geolocation.');
   infoWindow.open(map);
}