var pepe = [["https", 473], ["the", 273], ["you", 134], ["and", 128], ["for", 125], ["this", 109], ["irma", 85], ["n't", 71], ["that", 63], ["florida", 59], ["just", 58], ["hurricaneirma", 58], ["are", 56], ["out", 51], ["but", 50], ["power", 49], ["with", 49], ["have", 47], ["miami", 46], ["now", 44], ["hurricane", 44], ["not", 39], ["was", 38], ["amp", 38], ["good", 36], ["what", 36], ["our", 36], ["all", 35], ["from", 35], ["job", 35], ["can", 34], ["mph", 32], ["first", 31], ["football", 31], ["like", 29], ["hiring", 28], ["they", 27], ["about", 27], ["want", 26], ["storm", 26]];
function CreateWordCloud(dataSet){

jQuery('#word-cloud div').html('')
var config = {
    trace: false,
    spiralResolution: 1, //Lower = better resolution
    spiralLimit: 360 * 5,
    lineHeight: 0.8,
    xWordPadding: 0,
    yWordPadding: 3,
    font: "sans-serif"
}

var words = dataSet.map(function([word,value]) {
    console.log(value)
    return {
        word: word,
        freq: value*4
    }
})

/*words.sort(function(a, b) {
    return -1 * (a.freq - b.freq);
});*/

var cloud = document.getElementById("word-cloud");
console.log(cloud)
cloud.style.position = "relative";
cloud.style.fontFamily = config.font;

var traceCanvas;
var traceCanvasCtx;

var startPoint = {
    x: cloud.offsetWidth / 2,
    y: cloud.offsetHeight / 2
};

var wordsDown = [];

function setupCanvas(){
    traceCanvas = document.createElement("canvas");
    traceCanvas.width = cloud.offsetWidth;
    traceCanvas.height = cloud.offsetHeight;
    traceCanvasCtx = traceCanvas.getContext("2d");
    cloud.appendChild(traceCanvas);
}
/* ======================= END SETUP ======================= */





/* =======================  PLACEMENT FUNCTIONS =======================  */
function createWordObject(word, freq) {
    var wordContainer = document.createElement("div");
    wordContainer.style.position = "relative";
    wordContainer.style.fontSize = freq + "px";
    wordContainer.style.lineHeight = config.lineHeight;
/*    wordContainer.style.transform = "translateX(-50%) translateY(-50%)";*/
    wordContainer.appendChild(document.createTextNode(word));

    return wordContainer;
}

function placeWord(word, x, y) {

    cloud.appendChild(word);
    word.style.left = x - word.offsetWidth/2 + "px";
    word.style.top = y - word.offsetHeight/2 + "px";

    wordsDown.push(word.getBoundingClientRect());
}

function trace(x, y) {
//     traceCanvasCtx.lineTo(x, y);
//     traceCanvasCtx.stroke();
    traceCanvasCtx.fillRect(x, y, 1, 1);
}

function spiral(i, callback) {
    angle = config.spiralResolution * i;
    x = (1 + angle) * Math.cos(angle);
    y = (1 + angle) * Math.sin(angle);
    return callback ? callback() : null;
}

function intersect(word, x, y) {
    cloud.appendChild(word);

    word.style.left = x - word.offsetWidth/2 + "px";
    word.style.top = y - word.offsetHeight/2 + "px";

    var currentWord = word.getBoundingClientRect();

    cloud.removeChild(word);

    for(var i = 0; i < wordsDown.length; i+=1){
        var comparisonWord = wordsDown[i];

        if(!(currentWord.right + config.xWordPadding < comparisonWord.left - config.xWordPadding ||
             currentWord.left - config.xWordPadding > comparisonWord.right + config.wXordPadding ||
             currentWord.bottom + config.yWordPadding < comparisonWord.top - config.yWordPadding ||
             currentWord.top - config.yWordPadding > comparisonWord.bottom + config.yWordPadding)){

            return true;
        }
    }

    return false;
}
/* =======================  END PLACEMENT FUNCTIONS =======================  */





/* =======================  LETS GO! =======================  */
(function placeWords() {
    for (var i = 0; i < words.length; i += 1) {

        var word = createWordObject(words[i].word, words[i].freq);

        for (var j = 0; j < config.spiralLimit; j++) {
            //If the spiral function returns true, we've placed the word down and can break from the j loop
            if (spiral(j, function() {
                    if (!intersect(word, startPoint.x + x, startPoint.y + y)) {
                        placeWord(word, startPoint.x + x, startPoint.y + y);
                        return true;
                    }
                })) {
                break;
            }
        }
    }
})();
/* ======================= WHEW. THAT WAS FUN. We should do that again sometime ... ======================= */



/* =======================  Draw the placement spiral if trace lines is on ======================= */
(function traceSpiral() {

    traceCanvasCtx.beginPath();

    if (config.trace) {
        var frame = 1;

        function animate() {
            spiral(frame, function() {
                trace(startPoint.x + x, startPoint.y + y);
            });

            frame += 1;

            if (frame < config.spiralLimit) {
                window.requestAnimationFrame(animate);
            }
        }

        animate();
    }
})();
}

function getSessionId(){
    return $('#session-id').attr('content')
}

function displayTopTen(){
    var request = $.ajax({
        method: 'GET',
        url: '../WordFrequency.json?sessionId=' + getSessionId(),
        dataType: 'json'
    });

    request.done(function (json) {


        console.log(json)  //todo
        CreateWordCloud(json);
    });

    request.fail(function( jqXHR, textStatus ) {
        alert( "Request failed: " + textStatus );
    });
}